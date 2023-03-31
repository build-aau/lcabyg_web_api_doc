API
===
### About
Documentation, examples and use cases of the LCAby Web API.

Please be aware that the scope of underlying software architecture is broader than the LCAbyg Web API.

### Requirements


A valid account is needed to use the API. 
One can be created at <https://api.lcabyg.dk>. This will give you a USER_NAME and API_KEY.

After connecting to the server and logging into the API, an access TOKEN will be generated. 

### Endpoints

The provided api.csv file contains a list of the supported API endpoints.

### Examples

A python project / library is available to see how to use the API.

Download the Python examples to see how the API can be used and what format to send and expect to get back.
- example.py provides an example of submitting jobs to the API using the functions in the lcabyg_web_api_py and 
- sbi_web_api_py helper packages directly. Eventually these will be developed into Python libraries.
- example_explained.py reviews step-by-step how the API works without using the helper packages.

### Procedure

When using the API, you must connect to one of our servers.
Currently, there is only one: <https://api1.lcabyg.dk>
More will be added in the future to ensure redundancy.

The ping and ping_secure endpoints are provided to test whether the server works.
The first can be called without logging in, and the second can be reversed.

The first step is to login via the login endpoint.

Then one or more jobs can be submitted.
When submitting a job, the job data is returned, including the job id and the status.
Use this id to retrieve the job data to query for an updated status.

The job should either succeed or fail.
In the first case, the job results can be retrieved from the output endpoint.
In the second case, the reason for the failure can be retrieved in the 'extra_output' field of the job data.

Finally, you should mark the job as finished when you have all the data you need.

Please be aware that when the job is marked as finished, your job will be removed from the system sooner or later.


###  Login

There are three different ways of logging in.

The recommended way is to connect to the login endpoint and provide a `basic auth` compatible header.
Alternatively, one can provide the username and password via the body as json.
Lastly, and recommended only to be used if all other options fail, is to provide the username and password via a query string.

In all cases, if the login succeeds, a token is returned.
This is needed for all further API calls.
Notice: This token is only valid for the server you are connected to.
Notice: The token is returned as JSON and hence needs to be parsed as such (if you take it verbatim, you will get the quotations marks included).
Header / basic auth example:
See <https://datatracker.ietf.org/doc/html/rfc7617>

Body example:

```
{
    "username": "<YOUR USERNAME>",
    "password": "<YOUR PASSWORD>"
}
```

Query example:

```
https://api1.lcabyg.dk/v2/login?username=<YOUR USERNAME>&password=<YOUR PASSWORD>
```

###  Input Data

The input data should be provided as a json object like the following:

```
{
    "priority": 0,
    "job_target": "lcabyg5+br23",
    "job_target_min_ver": "",
    "job_target_max_ver": "",
    "job_arguments": "",
    "extra_input": "",
    "input_blob": <LCABYG_JSON_BLOB>,
}
```

The `job_target` should be `lcabyg5+br23` for LCAbyg 2023 calculations.
The input blob should be a valid LCAbyg 2023 JSON project, standard base64 encoded string. See <https://en.wikipedia.org/wiki/Base64>.
The arguments `priority`, `job_target_min_ver`, `job_target_max_ver`, `job_arguments`, `extra_input` is currently not used and should be empty strings.

The reason for this strange way of submitting a json project, is because this job queue system is used for more than just LCAbyg calculations.

###  Output Data

The data is returned as a standard base64 encoded string.
For LCAbyg, the decoded string is a json document.
Error messages are located in the output JSON data, "extra_output." We are currently working on improving the 
debug-functionality and provide more user-friendly error messages. 

### Job Status

Submitted jobs start with the status `New` and are queued.
When it is getting processed, the status changes to `Started`.
When a job succeeds, the status is `Ready`.
When a job fails, the status is `Failed`.
When a job is marked as finished by the user, the status is `Finished`.
Finally, if the user forgets to mark the job as finished, it will eventually be set to `Abandoned`.

### Limits

Your account is rate limited.
The details can be retrieved from the account endpoint.

job_target: the type of calculation these rules relates to.
max_jobs_in_queue: controls how many jobs you can have in the queue (that are not `Finished` or `Abandoned`).
max_running_jobs: controls how many jobs can be `New` or `Started`.
max_job_age: controls when a job is marked as `Abandoned`.
max_priority: currently not used.


