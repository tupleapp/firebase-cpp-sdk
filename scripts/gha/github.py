# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A utility for GitHub REST API.

This script handles GitHub Issue, Pull Request, Comment, Label and Artifact

"""

import requests
import json
import shutil

from absl import logging

OWNER = 'firebase'
REPO = 'firebase-cpp-sdk'

BASE_URL = 'https://api.github.com'
FIREBASE_URL = '%s/repos/%s/%s' % (BASE_URL, OWNER, REPO)
logging.set_verbosity(logging.INFO)

def create_issue(token, title, label):
  """Create an issue: https://docs.github.com/en/rest/reference/issues#create-an-issue"""
  url = f'{FIREBASE_URL}/issues'
  headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': f'token {token}'}
  data = {'title': title, 'labels': [label]}
  with requests.post(url, headers=headers, data=json.dumps(data)) as response:
    logging.info("create_issue: %s response: %s", url, response)
    return response.json()


def update_issue(token, issue_number, data):
  """Update an issue: https://docs.github.com/en/rest/reference/issues#update-an-issue"""
  url = f'{FIREBASE_URL}/issues/{issue_number}'
  headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': f'token {token}'}
  with requests.patch(url, headers=headers, data=json.dumps(data)) as response:
    logging.info("update_issue: %s response: %s", url, response)


def open_issue(token, issue_number):
  update_issue(token, issue_number, data={'state': 'open'})


def close_issue(token, issue_number):
  update_issue(token, issue_number, data={'state': 'closed'})


def update_issue_comment(token, issue_number, comment):
  update_issue(token, issue_number, data={'body': comment})


def search_issues_by_label(label):
  """https://docs.github.com/en/rest/reference/search#search-issues-and-pull-requests"""
  url = f'{BASE_URL}/search/issues?q=repo:{OWNER}/{REPO}+label:"{label}"+is:issue' 
  headers = {'Accept': 'application/vnd.github.v3+json'}
  with requests.get(url, headers=headers) as response:
    logging.info("search_issues_by_label: %s response: %s", url, response)
    return response.json()["items"]


def list_comments(issue_number):
  """https://docs.github.com/en/rest/reference/issues#list-issue-comments"""
  url = f'{FIREBASE_URL}/issues/{issue_number}/comments' 
  headers = {'Accept': 'application/vnd.github.v3+json'}
  with requests.get(url, headers=headers) as response:
    logging.info("list_comments: %s response: %s", url, response)
    return response.json()


def add_comment(token, issue_number, comment):
  """https://docs.github.com/en/rest/reference/issues#create-an-issue-comment"""
  url = f'{FIREBASE_URL}/issues/{issue_number}/comments' 
  headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': f'token {token}'}
  data = {'body': comment}
  with requests.post(url, headers=headers, data=json.dumps(data)) as response:
    logging.info("add_comment: %s response: %s", url, response)


def update_comment(token, comment_id, comment):
  """https://docs.github.com/en/rest/reference/issues#update-an-issue-comment"""
  url = f'{FIREBASE_URL}/issues/comments/{comment_id}' 
  headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': f'token {token}'}
  data = {'body': comment}
  with requests.patch(url, headers=headers, data=json.dumps(data)) as response:
    logging.info("update_comment: %s response: %s", url, response)


def delete_comment(token, comment_id):
  """https://docs.github.com/en/rest/reference/issues#delete-an-issue-comment"""
  url = f'{FIREBASE_URL}/issues/comments/{comment_id}' 
  headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': f'token {token}'}
  with requests.delete(url, headers=headers) as response:
    logging.info("delete_comment: %s response: %s", url, response)


def add_label(token, issue_number, label):
  """https://docs.github.com/en/rest/reference/issues#add-labels-to-an-issue"""
  url = f'{FIREBASE_URL}/issues/{issue_number}/labels' 
  headers={}
  headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': f'token {token}'}
  data = [label]
  with requests.post(url, headers=headers, data=json.dumps(data)) as response:
    logging.info("add_label: %s response: %s", url, response)


def delete_label(token, issue_number, label):
  """https://docs.github.com/en/rest/reference/issues#delete-a-label"""
  url = f'{FIREBASE_URL}/issues/{issue_number}/labels/{label}' 
  headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': f'token {token}'}
  with requests.delete(url, headers=headers) as response:
    logging.info("delete_label: %s response: %s", url, response)


def list_artifacts(token, run_id):
  """https://docs.github.com/en/rest/reference/actions#list-workflow-run-artifacts"""
  url = f'{FIREBASE_URL}/actions/runs/{run_id}/artifacts' 
  headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': f'token {token}'}
  with requests.get(url, headers=headers) as response:
    logging.info("list_artifacts: %s response: %s", url, response)
    return response.json()["artifacts"]


def download_artifact(token, artifact_id, output_path):
  """https://docs.github.com/en/rest/reference/actions#download-an-artifact"""
  url = f'{FIREBASE_URL}/actions/artifacts/{artifact_id}/zip' 
  headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': f'token {token}'}
  with requests.get(url, headers=headers, stream=True) as response:
    logging.info("download_artifact: %s response: %s", url, response)
    with open(output_path, 'wb') as file:
        shutil.copyfileobj(response.raw, file)
