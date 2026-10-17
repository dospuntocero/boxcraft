"""Extrae respuestas de troquel y estados por etapa de un bundle REA."""
import base64
import json
import sys
from pathlib import Path

bundle_path = Path(sys.argv[1])
evidence_id = sys.argv[2]
out = Path(__file__).resolve().parent / (sys.argv[3] if len(sys.argv) > 3 else 'experimentos')
out.mkdir(parents=True, exist_ok=True)
bundle = json.loads(bundle_path.read_text())
record = next(r for r in bundle['records'] if r['evidence_id'] == evidence_id)
result = record['normalized_result']
if 'error' in result:
    result = result['error']['details']['partial_observation']['capture']
events = result['events']['items']
requests = {e['transaction_id']: e for e in events if e['kind'] == 'request'}
steps = {s['step_index']: s for s in result['steps']}
samples = []
for e in events:
    request = requests.get(e.get('transaction_id'), {})
    url = request.get('url', {}).get('url', '')
    body = e.get('body', {})
    if e['kind'] != 'network-content' or '/project/knife?' not in url or body.get('state') != 'captured':
        continue
    parsed = json.loads(base64.b64decode(body['content']))
    if not isinstance(parsed.get('data'), dict) or 'knifeSize' not in parsed['data']:
        continue
    index = len(samples)
    filename = f'knife-{index:02}.json'
    (out / filename).write_text(json.dumps(parsed, indent=2, ensure_ascii=False))
    k = parsed['data']
    samples.append({'file': filename, 'request_step': request['step_index'], 'request_step_id': steps[request['step_index']]['step_id'], 'response_step': e['step_index'], 'url': url, 'body_sha256': body['sha256'], 'size': k['size'], 'knifeSize': k['knifeSize'], 'science': k['science']['name'], 'thickness': k['layer']['traditional']['thickness'], 'params': k['openParams']})
states = [{'id': s['step_id'], 'status': s['status'], 'error': s['error'], 'text': s['artifacts'].get('accessibility', {}).get('value', {}).get('text', '')} for s in result['steps']]
manifest = {'source_evidence_id': evidence_id, 'completeness': result.get('completeness', 'partial-error-capture'), 'samples': samples, 'states': states}
(out / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
for sample in samples:
    print(sample['file'], sample['request_step_id'], sample['knifeSize'], 'D=', sample['thickness'])
for state in states:
    if state['status'] != 'completed':
        print('ACTION', state['id'], state['status'], state['error'])
