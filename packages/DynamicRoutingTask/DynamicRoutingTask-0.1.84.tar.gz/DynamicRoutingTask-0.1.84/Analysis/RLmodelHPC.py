# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:37:16 2022

@author: svc_ccg
"""

import argparse
import itertools
import os
import pathlib
import random
import numpy as np
import pandas as pd
import scipy.optimize
import sklearn.metrics
from  DynamicRoutingAnalysisUtils import getFirstExperimentSession, getSessionsToPass, getSessionData


baseDir = pathlib.Path('//allen/programs/mindscope/workgroups/dynamicrouting')


def getSessionsToFit(mouseId,trainingPhase,sessionIndex):
    drSheets,nsbSheets = [pd.read_excel(os.path.join(baseDir,'DynamicRoutingTask',fileName),sheet_name=None) for fileName in ('DynamicRoutingTraining.xlsx','DynamicRoutingTrainingNSB.xlsx')]
    df = drSheets[str(mouseId)] if str(mouseId) in drSheets else nsbSheets[str(mouseId)]
    preExperimentSessions = np.array(['stage 5' in task for task in df['task version']]) & ~np.array(df['ignore'].astype(bool))
    firstExperimentSession = getFirstExperimentSession(df)
    if firstExperimentSession is not None:
        preExperimentSessions[firstExperimentSession:] = False
    preExperimentSessions = np.where(preExperimentSessions)[0]
    if trainingPhase in ('initial training','after learning'):
        if trainingPhase == 'initial training':
            sessions = preExperimentSessions[:5]
        elif trainingPhase == 'after learning':
            sessionsToPass = getSessionsToPass(mouseId,df,preExperimentSessions,stage=5)
            sessions = preExperimentSessions[sessionsToPass:sessionsToPass+5]
        testSession = sessions[sessionIndex]
        trainSessions = [s for s in sessions if s != testSession]
    else:
        sessions = np.array([trainingPhase in task for task in df['task version']]) & ~np.array(df['ignore'].astype(bool))
        sessions = np.where(sessions)[0]
        testSession = sessions[sessionIndex]
        trainSessions = preExperimentSessions[-4:]
    testData = getSessionData(mouseId,df.loc[testSession,'start time'])
    trainData = [getSessionData(mouseId,startTime) for startTime in df.loc[trainSessions,'start time']]
    return testData,trainData


def calcLogisticProb(q,tau,bias):
    return 1 / (1 + np.exp(-(q + bias) / tau))


def runModel(obj,tauAction,biasAction,visConfidence,audConfidence,alphaContext,alphaAction,alphaHabit,useHistory=True,nReps=1):
    stimNames = ('vis1','vis2','sound1','sound2')
    stimConfidence = [visConfidence,audConfidence]

    qStim = np.zeros((nResps,obj.nTrials,len(stimNames)))
    qStim[:,:,0] = 2 * visConfidence - 1
    qStim[:,:,1] = 2 * (1-visConfidence) - 1
    qStim[:,:,2] = 2 * audConfidence - 1
    qStim[:,:,3] = 2 * (1-audConfidence) - 1

    wContext = np.zeros((nResps,obj.nTrials))
    if alphaContext > 0:
        wContext += 0.5
    pContext = np.zeros((nReps,obj.nTrials,2)) + 0.5
    qContext = -np.ones((2,len(stimNames)))  
    qContext[0,:2] = qStim[0,0,:2].copy()
    qContext[1,-2:] = qStim[0,0,-2:].copy()

    wHabit = np.zeros((nResps,obj.nTrials))
    if alphaHabit > 0:
        wHabit += 0.5
    qHabit = qStim[0,0,:].copy()

    expectedValue = -np.ones((nReps,obj.nTrials))

    pAction = np.zeros((nReps,obj.nTrials))
    
    action = np.zeros((nReps,obj.nTrials),dtype=int)
    
    for i in range(nReps):
        for trial,stim in enumerate(obj.trialStim):
            if stim != 'catch':
                modality = 0 if 'vis' in stim else 1
                pStim = np.zeros(len(stimNames))
                pStim[[stim[:-1] in s for s in stimNames]] = [stimConfidence[modality],1-stimConfidence[modality]] if '1' in stim else [1-stimConfidence[modality],stimConfidence[modality]]
                
                valStim = np.sum(qStim[i,trial] * pStim)  
                
                valContext = np.sum(qContext * pStim[None,:] * pContext[i,trial][:,None])
                
                valHabit = np.sum(qHabit * pStim)

                expectedValue[i,trial] = wHabit[i,trial]*valHabit + (1-wHabit[i,trial]) * (wContext[i,trial]*valContext + (1-wContext[i,trial])*valStim)           
            
                pAction[i,trial] = calcLogisticProb(expectedValue[i,trial],tauAction,biasAction)
                
                if useHistory:
                    action[i,trial] = obj.trialResponse[trial]
                elif random.random() < pAction[i,trial]:
                    action[i,trial] = 1 
            
            if trial+1 < obj.nTrials:
                pContext[i,trial+1] = pContext[i,trial]
                qAction[i,trial+1] = qAction[i,trial]
                wHabit[i,trial+1] = wHabit[i,trial]
            
                if action[i,trial] or obj.autoRewarded[trial]:
                    outcome = 1 if obj.trialRewarded[trial] else -1
                    predictionError = outcome - expectedValue[i,trial]
                    
                    if alphaContext > 0 and stim != 'catch':
                        if outcome < 1:
                            contextError = -1 * pStim[0 if modality==0 else 2] * pContext[i,trial,modality]
                        else:
                            contextError = 1 - pContext[i,trial,modality] 
                        pContext[i,trial+1,modality] += contextError
                        pContext[i,trial+1,(1 if modality==0 else 0)] = 1 - pContext[i,trial+1,modality]
                        wContext[i,trial+1] += alphaContext * (0.5 * abs(contextError) - wContext[i,trial])
                    
                    if alphaAction > 0 and stim != 'catch':
                        qStim[i,trial+1] += alphaAction * pStim * predictionError
                        qStim[i,trial+1][qStim[i,trial+1] > 1] = 1 
                        qStim[i,trial+1][qStim[i,trial+1] < -1] = -1

                    if alphaHabit > 0:
                        wHabit[i,trial+1] += alphaHabit * (0.5 * abs(predictionError) - wHabit[i,trial])
    
    return pContext, qAction, expectedValue, wHabit, pAction, action


def evalModel(params,*args):
    trainData,fixedValInd,fixedVal = args
    if fixedVal is not None:
        params = np.insert(params,(fixedValInd[0] if isinstance(fixedValInd,tuple) else fixedValInd),fixedVal)
    response = np.concatenate([obj.trialResponse for obj in trainData])
    prediction = np.concatenate([runModel(obj,*params)[4][0] for obj in trainData])
    logLoss = sklearn.metrics.log_loss(response,prediction)
    return logLoss


def fitModel(mouseId,trainingPhase,testData,trainData):
    tauActionBounds = (0.01,1)
    biasActionBounds = (-1,1)
    visConfidenceBounds = (0.5,1)
    audConfidenceBounds = (0.5,1)
    alphaContextBounds = (0,1) 
    alphaActionBounds = (0,1)
    alphaHabitBounds = (0,1)

    bounds = (tauActionBounds,biasActionBounds,visConfidenceBounds,audConfidenceBounds,
              alphaContextBounds,alphaActionBounds,alphaHabitBounds)

    fixedValueIndices = (None,None,2,3,4,5,(4,5),6)
    fixedValues = (None,None,1,1,0,0,(0,0),0)

    fit = scipy.optimize.direct(evalModel,bounds,args=(trainData,None,None))
    params = [fit.x]
    logLoss = [fit.fun]
    for fixedValInd,fixedVal in zip(fixedValueIndices,fixedValues):
        if fixedVal is not None:
            bnds = tuple(b for i,b in enumerate(bounds) if (i not in fixedValInd if isinstance(fixedValInd,tuple) else i != fixedValInd))
            fit = scipy.optimize.direct(evalModel,bnds,args=(trainData,fixedValInd,fixedVal))
            params.append(np.insert(fit.x,(fixedValInd[0] if isinstance(fixedValInd,tuple) else fixedValInd),fixedVal))
            logLoss.append(fit.fun)

    fileName = str(mouseId)+'_'+testData.startTime+'_'+trainingPhase+'.npz'
    filePath = os.path.join(baseDir,'Sam','RLmodel',fileName)
    np.savez(filePath,params=params,logLoss=logLoss) 
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mouseId',type=int)
    parser.add_argument('--sessionIndex',type=int)
    parser.add_argument('--trainingPhase',type=str)
    args = parser.parse_args()
    trainingPhase = args.trainingPhase.replace('_',' ')
    testData,trainData = getSessionsToFit(args.mouseId,trainingPhase,args.sessionIndex)
    fitModel(args.mouseId,trainingPhase,testData,trainData)
