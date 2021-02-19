# Getting data from BigQuery

This is a script that gets the data from a BigQuery table using an HTTP endpoint from Cloud Functions. An example input is as follows :

```
{"lat":33,"lng":172.25,"time1":"2019-01-01","time2":"2019-02-01"}
```

#### Explanation of parameters

```lat``` is the desired latitude

```lng``` is the desired longitude

```time1``` and ```time2``` are the desired time endpoints between which the data is to be collected from the table.
