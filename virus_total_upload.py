#!/usr/bin/env python3
# coding:utf8

import requests
import argparse
import sys
import os.path
import vt
import time


def set_args_definition(parser):
  parser.add_argument(
    "--file", 
    help="the file you want to upload in virus total.",
  )

  return parser


def check_args_valid_or_exit(args):
  if not args.file:
    print ('args --file is missing, existing early...')
    sys.exit(-1)

  if not os.path.isfile(args.file):
    print ("args file '{}' is not a valid file, exiting early ...".format(args.file))  
    sys.exit(-1)


def get_env_vars_or_exit(env_key):
  value = os.getenv(env_key) 
  if not value:
    print ('ERROR: env var {} is missing, please provide it and try again ...'.format(env_key))
    sys.exit(-1)
  return value


def post_file_to_virus_total(runtime_vars):
  client = runtime_vars['vt_client'] 
  with open(runtime_vars['file_full_path'], "rb") as f:
    runtime_vars['scan_result'] = client.scan_file(f, wait_for_completion=True).results


def output_result(runtime_vars):

  print ("scan result file {} :".format(
    runtime_vars['file_full_path'])
  )

  for engine in runtime_vars['scan_result']:

    if 'undetected' in runtime_vars['scan_result'][engine]['category']:
 
      print("engine: {} category: {}".format(
          engine, 
          runtime_vars['scan_result'][engine]['category']
        )
      )

    elif 'type-unsupported' in runtime_vars['scan_result'][engine]['category']:
      print("WARNING: engine: {} category: {}".format(
          engine,
          runtime_vars['scan_result'][engine]['category']
        )
      )
    else:
      print("DANGEROUS: engine: {} category: {}".format(
          engine,       
          runtime_vars['scan_result'][engine]['category']
        )
      )



def main (args):
  clean_args = {}
  clean_args['file'] = args.file

  runtime_vars = {}
  runtime_vars['file_full_path'] = clean_args['file']

  runtime_vars['virus_total_api_key'] =\
    get_env_vars_or_exit("VIRUS_TOTAL_API_TOKEN")

  runtime_vars['vt_client'] = vt.Client(
    runtime_vars['virus_total_api_key']
  )

  post_file_to_virus_total(runtime_vars)
  output_result(runtime_vars)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  args = set_args_definition(parser)
  args = parser.parse_args()
  check_args_valid_or_exit(args)
  main(args)

