from google.cloud import bigquery
import logging
import time
from flask import jsonify
#logging.getLogger().setLevel(logging.INFO)
t0=time.time()

def bq_example(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    logging.info("First log after {} seconds".format(time.time()-t0))
    request_json=request.get_json()
    if request_json and 'lat' in request_json and 'lng' in request_json and 'time1' in request_json and 'time2' in request_json:
        logging.info('handling request')
        lat = int(request_json['lat']*100)
        lng = int(request_json['lng']*100)
        time1= request_json['time1']
        time2= request_json['time2']
    else:
        logging.info("malformed request")
    bq_client = bigquery.Client()

    job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("lng", "INT64",lng),
        bigquery.ScalarQueryParameter("lat", "INT64",lat),
        bigquery.ScalarQueryParameter("time1", "STRING",time1),
        bigquery.ScalarQueryParameter("time2", "STRING",time2)
        ]
    )
    QUERY = (
    """with subq as (select lat,lon,time,cdir,fdir from `era5.radiation_pc4_2019` where lon=@lng and lat=@lat )
    select array_agg(struct(t,cdir[OFFSET(time_offset)] as c,fdir[OFFSET(time_offset)] as f)) as pairs
    from subq, unnest(time) as t with offset as time_offset
    where date(t) between @time1 and @time2 """)
    query_job = bq_client.query(QUERY,job_config=job_config)
    results=query_job.result()
    logging.info("Response prepared after after {} seconds".format(time.time()-t0))
    #response=jsonify(results)
    data=[]
    for row in results:
        data.append(list(row))
    logging.info(data)
    return jsonify(data)
