# virus total upload script

use virus total api to upload files and required scan
script get file parameter, upload and parse api result

# usage

you need to setup an env vars with virus total api token 

```
export VIRUS_TOTAL_API_TOKEN="your api token" 
```

please note that community version have a rate limiting of 4 upload by minutes

once the env vars is setup and required lib are installed you can run the script this way
here with scanning the README file

```
./virus_total_upload.py --file README.md
```

# requirement

```
request
python-vs
```
