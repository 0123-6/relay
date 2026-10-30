"""Record a daily GitHub star total and render dependency-free sketch-style SVGs."""

import argparse
from datetime import date, datetime, timedelta, timezone
from html import escape
import json
import math
import os
from pathlib import Path
import re
import tempfile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HISTORY_PATH = PROJECT_ROOT / 'data/star-history.json'
CHART_PATHS = {
  'light': PROJECT_ROOT / 'assets/star-history.svg',
  'dark': PROJECT_ROOT / 'assets/star-history-dark.svg',
}
THEMES = {
  'light': {'paper': '#FFFCF4', 'ink': '#273A42', 'muted': '#76817D', 'grid': '#DCE2D8', 'line': '#208A70', 'star': '#E7B348'},
  'dark': {'paper': '#17212B', 'ink': '#E7EFEA', 'muted': '#9AADA8', 'grid': '#34453F', 'line': '#78DBB6', 'star': '#F1CB73'},
}


def require_integer(value, label, minimum=0):
  if type(value) is not int or value < minimum:
    raise ValueError(f'{label} must be an integer of at least {minimum}.')


def validate_history(history):
  if not isinstance(history, dict) or type(history.get('schema')) is not int or history['schema'] != 1:
    raise ValueError('Unsupported star history schema.')
  repository = history.get('repository')
  if repository is not None:
    if not isinstance(repository, dict):
      raise ValueError('Invalid repository identity.')
    require_integer(repository.get('id'), 'Repository ID', 1)
    if not isinstance(repository.get('name'), str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+', repository['name']) or repository['name'].split('/')[1] in {'.', '..'}:
      raise ValueError('Invalid repository name.')
  snapshots = history.get('snapshots')
  if not isinstance(snapshots, list) or (snapshots and repository is None):
    raise ValueError('Snapshots need a repository identity.')
  previous_date = None
  for snapshot in snapshots:
    if not isinstance(snapshot, dict) or not isinstance(snapshot.get('date'), str):
      raise ValueError('Invalid daily snapshot.')
    sample_date = date.fromisoformat(snapshot['date'])
    if sample_date.isoformat() != snapshot['date'] or (previous_date and sample_date <= previous_date):
      raise ValueError('Snapshot dates must be unique, canonical, and increasing.')
    require_integer(snapshot.get('stars'), 'Star count')
    previous_date = sample_date
  return history


def record_snapshot(history, metadata, sample_date):
  validate_history(history)
  repository = {'id': metadata.get('id'), 'name': metadata.get('full_name')}
  candidate = {'schema': 1, 'repository': repository, 'snapshots': []}
  validate_history(candidate)
  require_integer(metadata.get('stargazers_count'), 'GitHub star count')
  if history['repository'] and history['repository']['id'] != repository['id']:
    raise ValueError('History belongs to another repository; refusing to mix star counts.')
  snapshots = [dict(snapshot) for snapshot in history['snapshots']]
  observed_date = sample_date.isoformat()
  if snapshots and observed_date < snapshots[-1]['date']:
    raise ValueError('The latest snapshot is in the future; refusing to overwrite history.')
  snapshot = {'date': observed_date, 'stars': metadata['stargazers_count']}
  if snapshots and snapshots[-1]['date'] == observed_date:
    snapshots[-1] = snapshot
  else:
    snapshots.append(snapshot)
  candidate['snapshots'] = snapshots
  return validate_history(candidate)


def fetch_repository(repository_name, token):
  if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+', repository_name) or repository_name.split('/')[1] in {'.', '..'}:
    raise ValueError('GITHUB_REPOSITORY must have the form owner/repository.')
  headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'Relay-Star-History', 'X-GitHub-Api-Version': '2026-03-10'}
  if token:
    headers['Authorization'] = f'Bearer {token}'
  request = Request(f'https://api.github.com/repos/{repository_name}', headers=headers)
  try:
    with urlopen(request, timeout=30) as response:
      metadata = json.load(response)
  except HTTPError as error:
    raise RuntimeError(f'GitHub returned HTTP {error.code}; existing history was not updated.') from None
  except (URLError, TimeoutError) as error:
    raise RuntimeError('Could not reach GitHub; existing history was not updated.') from error
  if not isinstance(metadata, dict) or not isinstance(metadata.get('full_name'), str) or metadata['full_name'].casefold() != repository_name.casefold():
    raise ValueError('GitHub returned a different repository than requested.')
  return metadata


def render_chart(history, theme='light'):
  validate_history(history)
  colors = THEMES[theme]
  snapshots = history['snapshots']
  repository_name = history['repository']['name'] if history['repository'] else 'Relay / GitHub stars'
  repository_label = repository_name if len(repository_name) <= 76 else repository_name[:73] + '…'
  latest_count = f"{snapshots[-1]['stars']:,}" if snapshots else '—'
  last_date = snapshots[-1]['date'] if snapshots else None
  accessible_description = f'Daily GitHub star totals for {repository_name}. '
  accessible_description += f'{latest_count} stars on {last_date}.' if snapshots else 'No snapshots collected yet.'
  left, right, top, bottom = 78, 852, 150, 374
  elements = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="470" viewBox="0 0 900 470" role="img" aria-labelledby="chart-title chart-description">',
    '<title id="chart-title">Relay · Star history</title>',
    f'<desc id="chart-description">{escape(accessible_description)}</desc>',
    f'<rect x="1" y="1" width="898" height="468" rx="22" fill="{colors["paper"]}"/>',
    f'<path d="M24 8 Q7 10 8 29 L9 441 Q8 460 28 460 L874 461 Q892 460 891 440 L891 30 Q892 9 872 9 Z" fill="none" stroke="{colors["grid"]}" stroke-width="1.4"/>',
    '<style>text{font-family:"Segoe Print","Bradley Hand","Comic Sans MS",cursive} .small{font-size:13px} .tick{font-size:13px}</style>',
    f'<path d="m42 27 5 11 12 1-9 8 3 12-11-6-10 6 2-12-9-8 13-1Z" fill="none" stroke="{colors["star"]}" stroke-width="2.6" stroke-linejoin="round"/>',
    f'<text x="74" y="55" font-size="29" font-weight="700" fill="{colors["ink"]}">Star history</text>',
    f'<text x="34" y="91" class="small" fill="{colors["muted"]}">{escape(repository_label)}</text>',
    f'<text x="852" y="55" text-anchor="end" font-size="32" font-weight="700" fill="{colors["line"]}">{latest_count}</text>',
    f'<text x="852" y="81" text-anchor="end" class="small" fill="{colors["muted"]}">stars</text>',
  ]
  maximum_count = max((snapshot['stars'] for snapshot in snapshots), default=0)
  raw_step = max(1, maximum_count / 4)
  magnitude = 10 ** math.floor(math.log10(raw_step))
  step = math.ceil(next(multiplier * magnitude for multiplier in (1, 2, 2.5, 5, 10) if multiplier * magnitude >= raw_step))
  upper_count = max(4 * step, math.ceil(maximum_count * 1.08 / step) * step)
  for tick_value in range(0, upper_count + 1, step):
    tick_y = bottom - tick_value / upper_count * (bottom - top)
    elements.extend([
      f'<path d="M{left} {tick_y:.2f} Q465 {tick_y - 0.6:.2f} {right} {tick_y:.2f}" fill="none" stroke="{colors["grid"]}" stroke-width="1" stroke-dasharray="3 7"/>',
      f'<text x="{left - 15}" y="{tick_y + 4:.2f}" text-anchor="end" class="tick" fill="{colors["muted"]}">{tick_value:,}</text>',
    ])
  elements.append(f'<path d="M{left + 0.7} {top - 7} Q{left - 1} 258 {left} {bottom} Q461 {bottom + 1.3} {right + 4} {bottom - 0.2}" fill="none" stroke="{colors["ink"]}" stroke-width="1.6" stroke-linecap="round"/>')
  if snapshots:
    first_day = date.fromisoformat(snapshots[0]['date'])
    day_span = (date.fromisoformat(snapshots[-1]['date']) - first_day).days
    points = [
      (left + (date.fromisoformat(snapshot['date']) - first_day).days / day_span * (right - left) if day_span else (left + right) / 2,
       bottom - snapshot['stars'] / upper_count * (bottom - top))
      for snapshot in snapshots
    ]
    if len(points) > 1:
      line_path = 'M' + ' L'.join(f'{point_x:.2f} {point_y:.2f}' for point_x, point_y in points)
      area_path = line_path + f' L{points[-1][0]:.2f} {bottom} L{points[0][0]:.2f} {bottom} Z'
      elements.extend([
        f'<path d="{area_path}" fill="{colors["line"]}" fill-opacity="0.075"/>',
        f'<path d="{line_path}" fill="none" stroke="{colors["line"]}" stroke-width="1.2" opacity="0.32" transform="translate(0.65 -0.7)" stroke-linejoin="round"/>',
        f'<path d="{line_path}" fill="none" stroke="{colors["line"]}" stroke-width="3.1" stroke-linecap="round" stroke-linejoin="round"/>',
      ])
    visible_points = points if len(points) <= 36 else [points[-1]]
    for point_x, point_y in visible_points:
      elements.append(f'<circle cx="{point_x:.2f}" cy="{point_y:.2f}" r="3.4" fill="{colors["paper"]}" stroke="{colors["line"]}" stroke-width="2"/>')
    final_x, final_y = points[-1]
    elements.append(f'<circle cx="{final_x:.2f}" cy="{final_y:.2f}" r="5" fill="{colors["line"]}" stroke="{colors["paper"]}" stroke-width="2"/>')
    tick_offsets = sorted({round(day_span * fraction / 4) for fraction in range(5)}) if day_span else [0]
    for day_offset in tick_offsets:
      tick_x = left + day_offset / day_span * (right - left) if day_span else (left + right) / 2
      tick_day = first_day + timedelta(days=day_offset)
      text_anchor = 'start' if day_span and day_offset == 0 else 'end' if day_span and day_offset == day_span else 'middle'
      elements.append(f'<text x="{tick_x:.2f}" y="404" text-anchor="{text_anchor}" class="tick" fill="{colors["muted"]}">{tick_day.isoformat()}</text>')
    if len(points) == 1:
      elements.append(f'<text x="465" y="196" text-anchor="middle" font-size="17" fill="{colors["muted"]}">The first point. More days, more story.</text>')
  else:
    elements.extend([
      f'<text x="465" y="246" text-anchor="middle" font-size="22" fill="{colors["ink"]}">Waiting for the first snapshot</text>',
      f'<text x="465" y="277" text-anchor="middle" font-size="14" fill="{colors["muted"]}">Publish to GitHub, then run the Star history workflow.</text>',
    ])
  footer_date = f'Updated {last_date}' if last_date else 'No data yet'
  elements.extend([
    f'<text x="34" y="446" class="small" fill="{colors["muted"]}">Daily totals · UTC</text>',
    f'<text x="852" y="446" text-anchor="end" class="small" fill="{colors["muted"]}">{footer_date}</text>',
    '</svg>',
  ])
  return '\n'.join(elements) + '\n'


def write_if_changed(destination_path, content):
  if destination_path.is_file() and destination_path.read_text(encoding='utf-8') == content:
    return
  destination_path.parent.mkdir(parents=True, exist_ok=True)
  with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='\n', dir=destination_path.parent, prefix='.star-history-', delete=False) as temporary_file:
    temporary_file.write(content)
    temporary_path = Path(temporary_file.name)
  temporary_path.chmod(0o644)
  os.replace(temporary_path, destination_path)


def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--render-only', action='store_true', help='Render existing records without contacting GitHub.')
  arguments = parser.parse_args()
  history = validate_history(json.loads(HISTORY_PATH.read_text(encoding='utf-8')))
  if not arguments.render_only:
    repository_name = os.environ.get('GITHUB_REPOSITORY', '')
    if not repository_name:
      raise ValueError('GITHUB_REPOSITORY is required when collecting a snapshot.')
    metadata = fetch_repository(repository_name, os.environ.get('GITHUB_TOKEN', ''))
    history = record_snapshot(history, metadata, datetime.now(timezone.utc).date())
  outputs = {chart_path: render_chart(history, theme) for theme, chart_path in CHART_PATHS.items()}
  if not arguments.render_only:
    outputs[HISTORY_PATH] = json.dumps(history, ensure_ascii=False, indent=2) + '\n'
  for destination_path, content in outputs.items():
    write_if_changed(destination_path, content)
  print(f'Star history: {len(history["snapshots"])} daily snapshots; charts updated.')


if __name__ == '__main__':
  try:
    main()
  except (ValueError, RuntimeError, OSError) as error:
    raise SystemExit(str(error)) from None
