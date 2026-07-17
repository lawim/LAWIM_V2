#!/usr/bin/env python3
"""Validate the LAWIM conversation dataset."""
import json, os, sys
from collections import Counter

VALID_INTENTS = None  # dynamic check
VALID_AGENTS = None  # dynamic
VALID_LANGS = {'fr','en','pcm'}
VALID_ROLES = {'user','assistant','system'}
VALID_CHANNELS = None  # dynamic

data_dir = sys.argv[1] if len(sys.argv) > 1 else 'datasets/conversation/lawim_conversation_corpus_1250'
errors = []
total = 0

for split in ['train.jsonl','dev.jsonl','test.jsonl']:
    path = os.path.join(data_dir, split)
    if not os.path.exists(path):
        errors.append(f'Missing: {split}')
        continue
    with open(path) as f:
        convs = [json.loads(l) for l in f if l.strip()]
    total += len(convs)
    for conv in convs:
        cid = conv.get('id','')
        lang = conv.get('language','')
        intent = conv.get('intent','')
        agent = conv.get('expected_agent','')
        channel = conv.get('channel','')
        if not cid: errors.append(f'{split}: missing id')
        if lang not in VALID_LANGS: errors.append(f'{cid}: invalid lang {lang}')
        if intent not in VALID_INTENTS: errors.append(f'{cid}: invalid intent {intent}')
        if agent not in VALID_AGENTS: errors.append(f'{cid}: invalid agent {agent}')
        if channel not in VALID_CHANNELS: errors.append(f'{cid}: invalid channel {channel}')
        msgs = conv.get('messages',[])
        if not msgs: errors.append(f'{cid}: no messages')
        for msg in msgs:
            if msg.get('role') not in VALID_ROLES: errors.append(f'{cid}: bad role')
            if not msg.get('content','').strip(): errors.append(f'{cid}: empty msg')

print(f'Total: {total}')
print(f'Errors: {len(errors)}')
for e in errors[:20]: print(f'  {e}')
if errors: sys.exit(1)
print('DATASET VALIDATION: PASS')
