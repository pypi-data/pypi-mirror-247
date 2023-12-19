#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 14:47:48 2023

@author: samgale
"""

import copy
import glob
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['pdf.fonttype'] = 42
from DynamicRoutingAnalysisUtils import getSessionData
from RLmodelHPC import calcLogisticProb, runModel


# plot relationship bewtween tau and q values
q = np.arange(-1,1.01,0.01)
tau = np.arange(0.01,2.01,0.01)
bias = (0,0.5)
xticks = np.arange(0,q.size+1,int(q.size/4))
yticks = np.arange(0,tau.size+1,int(tau.size/4))
yticks[1:] -= 1
for b in bias:
    p = np.zeros((tau.size,q.size))
    for i,t in enumerate(tau):
        p[i] = calcLogisticProb(q,t,b)
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    im = ax.imshow(p,clim=(0,1),cmap='magma',origin='lower',aspect='auto')
    ax.set_xticks(xticks)
    ax.set_xticklabels(np.round(q[xticks],1))
    ax.set_yticks(yticks)
    ax.set_yticklabels(tau[yticks])
    ax.set_xlabel('Q')
    ax.set_ylabel('temperature')
    ax.set_title('lick probability, bias='+str(b))
    plt.colorbar(im)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for t,clr in zip((0.1,0.2,0.4),'rgb'):
    for b,ls in zip(bias,('-','--')):
        ax.plot(q,calcLogisticProb(q,t,b),color=clr,ls=ls,label='temperature='+str(t)+', bias='+str(b))
for side in ('right','top'):
    ax.spines[side].set_visible(False)
ax.tick_params(direction='out',top=False,right=False,labelsize=12)
ax.set_xticks(np.arange(-1,1.1,0.5))
ax.set_yticks(np.arange(0,1.1,0.5))
ax.set_xlim([-1,1])
ax.set_ylim([0,1])
ax.set_xlabel('Q',fontsize=14)
ax.set_ylabel('lick probability',fontsize=14)
ax.legend()
plt.tight_layout()


# get fit params from HPC output
trainingPhases = ('initial training','after learning')
contextModes = ('no context','switch context','weight context')
qModes = ('q update','no q update')
modelData = {phase: {context: {q: {} for q in qModes} for context in contextModes} for phase in trainingPhases}
filePaths = glob.glob(os.path.join(r"\\allen\programs\mindscope\workgroups\dynamicrouting\Sam\RLmodel",'*.npz'))
for f in filePaths:
    mouseId,sessionDate,sessionTime,trainingPhase,contextMode,qMode,job = os.path.splitext(os.path.basename(f))[0].split('_')
    session = sessionDate+'_'+sessionTime
    data = modelData[trainingPhase][contextMode][qMode]
    with np.load(f) as d:
        params = d['params']
        logLoss = float(d['logLoss'])
    if mouseId not in data:
        data[mouseId] = {session: {'params': params, 'logLoss': logLoss}}
    elif session not in data[mouseId]:
        data[mouseId][session] = {'params': params, 'logLoss': logLoss}
    elif logLoss < data[mouseId][session]['logLoss']:
        data[mouseId][session]['params'] = params
        data[mouseId][session]['logLoss'] = logLoss


# get experiment data and model prediction
sessionData = {phase: {} for phase in trainingPhases}        
for trainingPhase in trainingPhases:
    for contextMode in contextModes:
        for qMode in qModes:
            d = modelData[trainingPhase][contextMode][qMode]
            if len(d) > 0:
                for mouse in d:
                    for session in d[mouse]:
                        obj = getSessionData(mouse,session)
                        d[mouse][session]['response'] = runModel(obj,contextMode,*d[mouse][session]['params'],useHistory=True,nReps=1)[3][0]
                        if mouse not in sessionData[trainingPhase]:
                            sessionData[trainingPhase][mouse] = {session: obj}
                        elif session not in sessionData[trainingPhase][mouse]:
                            sessionData[trainingPhase][mouse][session] = obj
                            

# plot logloss
clrs = 'krgbmc'
clrInd = 0
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for trainingPhase in trainingPhases:
    for contextMode in contextModes:
        for qMode in qModes:
            d = modelData[trainingPhase][contextMode][qMode]
            if len(d) > 0:
                logLoss = np.array([session['logLoss'] for mouse in d.values() for session in mouse.values()])
                dsort = np.sort(logLoss)
                cumProb = np.array([np.sum(dsort<=i)/dsort.size for i in dsort])
                lbl = trainingPhase+', '+contextMode+', '+qMode
                ax.plot(dsort,cumProb,color=clrs[clrInd],label=lbl)
                clrInd += 1
for side in ('right','top'):
    ax.spines[side].set_visible(False)
ax.tick_params(direction='out',top=False,right=False)
ax.set_ylim([0,1.01])
ax.set_xlabel('log loss')
ax.legend(bbox_to_anchor=(1,1))
plt.tight_layout()
                
                
# plot fit param values
paramNames = ('visConf','audConf','tauAction','biasAction','penalty','alphaContext','alphaAction')
clrs = 'krgbmc'
clrInd = 0
fig,axs = plt.subplots(len(paramNames),1,figsize=(8,10))
for trainingPhase in trainingPhases:
    for contextMode in contextModes:
        for qMode in qModes:
            d = modelData[trainingPhase][contextMode][qMode]
            if len(d) > 0:
                params = np.array([session['params'] for mouse in d.values() for session in mouse.values()]).T
                for i,p, in enumerate(params):
                    dsort = np.sort(p)
                    cumProb = np.array([np.sum(dsort<=i)/dsort.size for i in dsort])
                    lbl = trainingPhase+', '+contextMode+', '+qMode if i==0 else None
                    axs[i].plot(dsort,cumProb,color=clrs[clrInd],label=lbl)
                clrInd += 1
for ax,xlbl in zip(axs,paramNames):
    for side in ('right','top'):
        ax.spines[side].set_visible(False)
    ax.tick_params(direction='out',top=False,right=False)
    if 'Conf' in xlbl:
        ax.set_xlim([0.55,1])
    ax.set_ylim([0,1.01])
    ax.set_xlabel(xlbl)
axs[0].legend(bbox_to_anchor=(1,1))
plt.tight_layout()


# compare model and mice
stimNames = ('vis1','vis2','sound1','sound2')

preTrials = 5
postTrials = 15
x = np.arange(-preTrials,postTrials+1)
for trainingPhase in trainingPhases:
    fig = plt.figure(figsize=(8,8))
    a = 0
    for src in ('mice','model'):
        for contextMode in ((None,) if src=='mice' else modelData[trainingPhase].keys()):
            for qMode in ((None,) if src=='mice' else modelData[trainingPhase][contextMode].keys()):
                if src == 'mice':
                    d = sessionData[trainingPhase]
                else:
                    d = modelData[trainingPhase][contextMode][qMode]
                if len(d) == 0:
                    continue
                for rewardStim,blockLabel in zip(('vis1','sound1'),('visual rewarded blocks','sound rewarded blocks')):
                    ax = fig.add_subplot(6,2,a+1)
                    a += 1
                    for stim,clr,ls in zip(stimNames,'ggmm',('-','--','-','--')):
                        y = []
                        for mouse in d:
                            y.append([])
                            for session in d[mouse]:
                                obj = sessionData[trainingPhase][mouse][session]
                                if src == 'mice':
                                    resp = obj.trialResponse
                                else:
                                    resp = d[mouse][session]['response']
                                for blockInd,rewStim in enumerate(obj.blockStimRewarded):
                                    if rewStim==rewardStim and blockInd > 0:
                                        trials = (obj.trialStim==stim) & ~obj.autoRewardScheduled
                                        y[-1].append(np.full(preTrials+postTrials+1,np.nan))
                                        pre = resp[(obj.trialBlock==blockInd) & trials]
                                        i = min(preTrials,pre.size)
                                        y[-1][-1][:i] = pre[-i:]
                                        post = resp[(obj.trialBlock==blockInd+1) & trials]
                                        i = min(postTrials,post.size)
                                        y[-1][-1][preTrials+1:preTrials+1+i] = post[:i]
                            y[-1] = np.nanmean(y[-1],axis=0)
                        m = np.nanmean(y,axis=0)
                        s = np.nanstd(y,axis=0)/(len(y)**0.5)
                        ax.plot(x,m,color=clr,ls=ls,label=stim)
                        ax.fill_between(x,m+s,m-s,color=clr,alpha=0.25)
                    for side in ('right','top'):
                        ax.spines[side].set_visible(False)
                    ax.tick_params(direction='out',top=False,right=False)
                    ax.set_xticks(np.arange(-5,20,5))
                    ax.set_yticks([0,0.5,1])
                    ax.set_xlim([-preTrials-0.5,postTrials+0.5])
                    ax.set_ylim([0,1.01])
                    ax.set_xlabel('Trials after block switch')
                    ax.set_ylabel('Response rate')
                    if a==1:
                        ax.legend(loc='upper right')
                    title = 'mice, '+blockLabel+' (n='+str(len(y))+')' if src=='mice' else contextMode+', '+qMode
                    ax.set_title(title)
    plt.tight_layout()


respRate = {contextMode: {lbl: [] for lbl in ('rewarded target stim','unrewarded target stim')} for contextMode in ('mice',)+contextModes}
preTrials = 5
postTrials = 15
x = np.arange(-preTrials,postTrials+1)    
for stage in stages: 
    fig = plt.figure(figsize=(8,8))
    a = 0
    for contextMode in ('mice',) + contextModes:
        if stage=='early' and contextMode=='weight':
            continue
        ax = fig.add_subplot(3,1,a+1)
        ax.plot([0,0],[0,1],'--',color='0.5')
        for lbl,clr in zip(('rewarded target stim','unrewarded target stim'),'gm'):
            y = []
            for i,exps in enumerate(expsByMouse):
                if len(exps)>0:
                    # exps = exps[:5] if stage=='early' else exps[passSession[i]:passSession[i]+5]
                    y.append([])
                    for j,obj in enumerate(exps):
                        if contextMode == 'mice':
                            resp = obj.trialResponse
                        else:
                            resp = np.array(modelResponse[stage][contextMode][i][j])
                        for blockInd,rewStim in enumerate(obj.blockStimRewarded):
                            if blockInd > 0:
                                stim = np.setdiff1d(obj.blockStimRewarded,rewStim) if 'unrewarded' in lbl else rewStim
                                trials = (obj.trialStim==stim) & ~obj.autoRewardScheduled
                                y[-1].append(np.full(preTrials+postTrials+1,np.nan))
                                pre = resp[(obj.trialBlock==blockInd) & trials]
                                k = min(preTrials,pre.size)
                                y[-1][-1][:k] = pre[-k:]
                                post = resp[(obj.trialBlock==blockInd+1) & trials]
                                k = min(postTrials,post.size)
                                y[-1][-1][preTrials+1:preTrials+1+k] = post[:k]
                    y[-1] = np.nanmean(y[-1],axis=0)
            respRate[contextMode][lbl] = np.array(y)
            m = np.nanmean(y,axis=0)
            s = np.nanstd(y,axis=0)/(len(y)**0.5)
            ax.plot(x,m,color=clr,label=lbl)
            ax.fill_between(x,m+s,m-s,color=clr,alpha=0.25)
        for side in ('right','top'):
            ax.spines[side].set_visible(False)
        ax.tick_params(direction='out',top=False,right=False,labelsize=12)
        ax.set_xticks(np.arange(-preTrials,postTrials+1,5))
        ax.set_yticks([0,0.5,1])
        ax.set_xlim([-preTrials-0.5,postTrials+0.5])
        ax.set_ylim([0,1.01])
        if a==2:
            ax.set_xlabel('Trials of indicated type after block switch (auto-rewards excluded)',fontsize=12)
        ax.set_ylabel('Response rate',fontsize=12)
        if contextMode=='mice':
            title = str(len(y))+' mice'
        elif contextMode=='none':
            title = 'Q learning model'
        else:
            title = 'Q learning with context belief model'
        ax.set_title(title,fontsize=12)
        if a==0:
            ax.legend(bbox_to_anchor=(1,1))
        a += 1
    plt.tight_layout()
    

fig = plt.figure(figsize=(6,8))
for i,contextMode in enumerate(respRate.keys()):
    ax = fig.add_subplot(3,1,i+1)
    ax.plot([0.5,0.5],[0,1],'k--')
    for lbl,clr in zip(respRate[contextMode].keys(),'gm'):
        rr = respRate[contextMode][lbl][:,[preTrials-1,preTrials+1]]
        for r in rr:
            ax.plot([0,1],r,'o-',color=clr,mec=clr,mfc='none',ms=5,alpha=0.1)
        mean = np.mean(rr,axis=0)
        sem = np.std(rr,axis=0)/(len(rr)**0.5)
        ax.plot([0,1],mean,'o-',color=clr,ms=10,label=lbl)
        for x,m,s in zip([0,1],mean,sem):
            ax.plot([x,x],[m-s,m+s],color=clr)
    for side in ('right','top'):
        ax.spines[side].set_visible(False)
    ax.tick_params(direction='out',top=False,right=False,labelsize=12)
    ax.set_xticks([0,1])
    ax.set_xticklabels(['last trial before\nblock switch','first trial after\nblock switch'])
    ax.set_yticks([0,0.5,1])
    ax.set_xlim([-0.25,1.25])
    ax.set_ylim([0,1.01])
    ax.set_ylabel('Response rate',fontsize=12)
    if contextMode=='mice':
        title = str(len(y))+' mice'
    elif contextMode=='none':
        title = 'Q learning model'
    else:
        title = 'Q learning with context belief model'
    ax.set_title(title,fontsize=12)
    if a==0:
        ax.legend(bbox_to_anchor=(1,1))
plt.tight_layout()


    
# plot Q values
Qcontext = {stage: {context: [] for context in contextModes} for stage in stages}
Qaction = copy.deepcopy(Qcontext)
Qweight = copy.deepcopy(Qcontext)
pVis = copy.deepcopy(Qcontext)
pLick = copy.deepcopy(Qcontext)
for s,stage in enumerate(stages):
    for i,contextMode in enumerate(contextModes):
        if stage=='early' and contextMode=='weight':
            continue
        for j,exps in enumerate(expsByMouse):
            exps = exps[:5] if stage=='early' else exps[passSession[j]:passSession[j]+5]
            Qcontext[stage][contextMode].append([])
            Qaction[stage][contextMode].append([])
            Qweight[stage][contextMode].append([])
            pVis[stage][contextMode].append([])
            pLick[stage][contextMode].append([])
            for k,testExp in enumerate(exps):
                print(s,i,j,k)
                fitParams = modelParams[stage][contextMode][j][k]
                qc = []
                qa = []
                qw = []
                pv = []
                pl = []
                for _ in range(5):
                    c,a = runModel([testExp],contextMode,*fitParams)[1:]
                    qa.append(a[0])
                    if contextMode !='none':
                        qc.append(c[0])
                        pc = np.array([softmax(q,fitParams[0]) for q in c[0]])
                        qw.append(np.sum(a[0][:,:,[0,2],1] * pc[:,:,None],axis=1))
                        pv.append(pc[:,0])
                        pl.append(np.array([[softmaxWithBias(q,*fitParams[2:4]) for q in qq] for qq in qw[-1]])) 
                Qcontext[stage][contextMode][-1].append(np.mean(qc,axis=0))
                Qaction[stage][contextMode][-1].append(np.mean(qa,axis=0))
                Qweight[stage][contextMode][-1].append(np.mean(qw,axis=0))
                pVis[stage][contextMode][-1].append(np.mean(pv,axis=0))
                pLick[stage][contextMode][-1].append(np.mean(pl,axis=0))

preTrials = 20
postTrials = 70
x = np.arange(-preTrials,postTrials)    
for stage in stages:
    fig = plt.figure(figsize=(8,6))
    a = 0
    for contextMode in contextModes:
        if stage=='early' and contextMode=='weight':
            continue
        for rewardStim,blockLabel in zip(('vis1','sound1'),('visual','auditory')):
            ax = fig.add_subplot(2,2,a+1)
            a += 1
            ax.plot([0,0],[-1,1],':',color='0.7')
            ax.plot([-preTrials-0.5,postTrials+0.5],[0,0],':',color='0.7')
            lines = (('Qv','Qa'),'gm',('-','-')) if contextMode=='none' else (('Q vis context','Qwv','Qwa','Qvv','Qva','Qav','Qaa'),'kbrgmgm',('-','-','-','-','--','--','-'))
            for lbl,clr,ls in zip(*lines):
                y = []
                for i,exps in enumerate(expsByMouse):
                    exps = exps[:5] if stage=='early' else exps[passSession[i]:passSession[i]+5]
                    for j,obj in enumerate(exps):
                        if lbl=='Q vis context':
                            d = Qcontext[stage][contextMode][i][j][:,0]
                        elif lbl=='Qwv':
                            d = Qweight[stage][contextMode][i][j][:,0]
                        elif lbl=='Qwa':
                            d = Qweight[stage][contextMode][i][j][:,1]
                        else:
                            d = Qaction[stage][contextMode][i][j]
                            if lbl in ('Qv','Qvv'):
                                d = d[:,0,0,1]
                            elif lbl in ('Qa','Qva'):
                                d = d[:,0,2,1]
                            elif lbl=='Qav':
                                d = d[:,1,0,1]
                            elif lbl=='Qaa':
                                d = d[:,1,2,1]
                        for blockInd,rewStim in enumerate(obj.blockStimRewarded):
                            if blockInd > 0 and rewStim==rewardStim:
                                y.append(np.full(preTrials+postTrials,np.nan))
                                pre = d[obj.trialBlock==blockInd]
                                k = min(preTrials,pre.size)
                                y[-1][:k] = pre[-k:]
                                post = d[obj.trialBlock==blockInd+1]
                                k = min(postTrials,post.size)
                                y[-1][preTrials:preTrials+k] = post[:k]
                m = np.nanmean(y,axis=0)
                s = np.nanstd(y,axis=0)/(len(y)**0.5)
                ax.plot(x,m,color=clr,ls=ls,label=lbl)
                ax.fill_between(x,m+s,m-s,color=clr,alpha=0.25)
            for side in ('right','top'):
                ax.spines[side].set_visible(False)
            ax.tick_params(direction='out',top=False,right=False,labelsize=12)
            ax.set_xlim([-preTrials-0.5,postTrials+0.5])
            ax.set_ylim([-1.01,1.01])
            if (stage=='early' and contextMode=='none') or contextMode=='weight':
                ax.set_xlabel('Trials from block switch',fontsize=12)
            if blockLabel=='visual':
                ax.set_ylabel('Q',fontsize=12)
            if contextMode=='none':
                title = blockLabel+' rewarded blocks\n'+'Q learning'
            else:
                title = 'Q learning with context belief'
            ax.set_title(title,fontsize=12)
            if blockLabel=='auditory':
                ax.legend(bbox_to_anchor=(1,1),loc='upper left')
    plt.tight_layout()




