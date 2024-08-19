#!/usr/bin/env python

import os
import sys
import argparse
import json
import logging
import subprocess
import difflib

def config_logger():
    LOG_FORMAT = '%(asctime)s %(levelname)s [%(name)s] %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    logging.basicConfig(level=logging.INFO,
                        format=LOG_FORMAT, datefmt=DATE_FORMAT)

config_logger()

def read_output(path):
    with open(path, 'r') as f:
        return f.read().strip()

def run_case(dir, image, tool_path, verbose: bool = False):
    assert os.path.isabs(dir)
    assert os.path.isabs(tool_path)

    docker_dir = '/testcase'
    docker_tool_path = '/tool'

    cmd = f'''\
docker run -t \
    --device /dev/fuse --cap-add SYS_ADMIN --security-opt apparmor:unconfined \
    -v {dir}:{docker_dir} \
    -v {tool_path}:{docker_tool_path} \
    {image} \
    sudo {docker_tool_path} \
        --no-npe-good-source --no-nodes \
        {docker_dir}/input.json \
'''
    logging.info(f"Running command: {cmd}")

    output_path = os.path.join(dir, 'output.json')
    original_output = read_output(output_path)
    os.remove(output_path)
    if verbose:
        subprocess.run(cmd, shell=True, check=True)
    else:
        subprocess.run(cmd, shell=True, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    new_output = read_output(output_path)
    if original_output != new_output:
        logging.error(f"  Output mismatch: {dir}")

        diff = difflib.unified_diff(
            original_output.splitlines(keepends=True),
            new_output.splitlines(keepends=True),
            fromfile='intented output',
            tofile='actual output'
        )
        # 打印差异
        print(''.join(diff))
        sys.stdout.flush()

        raise Exception(f"Output mismatch: {dir}")

def update_paths(root, src):
    dst = '/testcase'
    logging.info(f'Updating paths: {src} -> {dst}')
    cmd = f'''
    sed -i 's|{src}|{dst}|g' $(find {root} -type f -name '*.json')
'''
    subprocess.run(cmd, shell=True, check=True)

def run(root, tool, verbose):
    logging.info(f"Test case directory: {root}")
    for file in ['input.json', 'output.json']:
        assert os.path.exists(os.path.join(root, file)), f"{file} does not exist"

    logging.info(f'Tool AppImage path: {tool}')
    assert os.path.exists(tool), "Tool AppImage does not exist"
    assert os.access(tool, os.X_OK), "Tool AppImage is not executable"

    with open(os.path.join(root, 'input.json')) as f:
        data = json.load(f)
        assert 'docker' in data
        image_name = data['docker']
        assert image_name.startswith('thebesttv/vul-manual:')
        logging.info(f"Image name: {image_name}")

    with open(os.path.join(root, 'output.json')) as f:
        data = json.load(f)
        assert 'source' in data
        source = data['source']
        assert source.endswith('/input.json')
        source = source[:-len('/input.json')] # remove suffix
        logging.info(f"Source: {source}")

    update_paths(root, source)
    run_case(root, image_name, tool, verbose)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='test.py',
        description='Test script for manual dataset (repo: vul-manual-ga)'
    )
    parser.add_argument('tool', type=str,
                        help='Path to path-generation tool (AppImage)')
    parser.add_argument('-d', '--dir', type=str, default=os.getcwd(),
                        help='Test case directory, default to cwd')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Show tool output')

    args = parser.parse_args()

    run(os.path.abspath(args.dir), os.path.abspath(args.tool), args.verbose)
