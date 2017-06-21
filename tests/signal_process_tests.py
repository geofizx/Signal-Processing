#!/usr/bin/env python2.7
# encoding: utf-8

"""
Some tests and usage examples for signal processing library

@Usage Examples and Tests
Run tests for primary periods of multiple time-series data
Run tests for time registration of multiple time-series data
Run tests for timeRegister of multiple series input
Run despike with 30-sample window given min periodicity
Run replacement test
Generate plots for some outputs

@author Michael Tompkins
@copyright 2016
"""

import numpy as npy
from datetime import datetime
import json
import time
import matplotlib.pyplot as plt
from code import signalProcess

# Determine which tests will be run with bools
run_period = False
run_time_register = False
run_depike = True
run_replace = True

print "Loading some time-series data\n"
t_st = time.time()
filename = "three_time_series_data.json"
data_in = {"data":{},"time":{}}
file1 = open(filename,"r")
data1 = json.load(file1)
for name in data1["data"]:
	data_in["data"][name] = npy.asfarray(data1["data"][name]).tolist()
	data_in["time"][name] = data1["time"][name]

print "Time-Series Labels: ",data_in["data"].keys()
t_en = time.time()
print "Data Load Time:",t_en - t_st,"\n"

# Run the unit tests
if run_period is True:
	"""
	Get primary periods from three time series
	"""
	t_st = time.time()
	options = None
	lrner = signalProcess(data_in,options)
	output = lrner.getPrimaryPeriods()
	t_en = time.time()
	print "Primary Periodicity and SNR Processing Time: ",t_en - t_st," secs"
	for key in output:
		print "Signal Property Results: ",key
		for keyname in output[key]:
			print keyname,output[key][keyname]

if run_time_register is True:

	"""
	Resample all time series to mean sampling rate shared for all series. First call resamples to mean sampling rate
	and the second call down samples this mean sampling rate by a factor of 50
	"""

	t_st = time.time()

	# Run with no down-sampling
	options = {"sample":1}
	lrner = signalProcess(data_in,options)
	data_out, params_out = lrner.registerTime()
	datetime_vals = [datetime.fromtimestamp(int(it)) for it in data_out["time"]]
	plt.subplot(2,1,1)
	plt.title("Resampled time series at mean sampling rate of all series")
	for key in data_out["data"]:
		plt.hold(True)
		plt.plot(datetime_vals,data_out["data"][key],label=key)
		plt.legend()

	# Run again with 50x down-sampling
	options = {"sample":50}
	lrner = signalProcess(data_in,options)
	data_out, params_out = lrner.registerTime()
	t_en = time.time()
	print "Resampling Processing Time: ",t_en - t_st," secs\n"
	datetime_vals = [datetime.fromtimestamp(int(it)) for it in data_out["time"]]
	plt.subplot(2,1,2)
	plt.title("Resampled time series at 50x down-sampled mean sampling rate")
	for key in data_out["data"]:
		plt.hold(True)
		plt.plot(datetime_vals,data_out["data"][key],label=key)
		plt.legend()
	plt.show()

if run_depike is True:

	"""
	Run despike only on key : "time_serie3". With 30-sample local despike search window

	"""
	data3 = {"data":{"time_series3":data_in["data"]["time_series3"]},
			 "time":{"time_series3":data_in["time"]["time_series3"]}}

	t_st = time.time()
	options = {"window":31}
	lrner = signalProcess(data3,options)
	data_out = lrner.despikeSeries()
	t_en = time.time()
	print "Despike Processing Time: ",t_en - t_st," secs\n"

	# plot before and after
	datetime_vals = [datetime.fromtimestamp(int(it)) for it in data_out["time"]["time_series3"]]
	for key in data_out["data"]:
		plt.hold(True)
		plt.plot(datetime_vals,data_in["data"][key],label="Original Data")
		plt.plot(datetime_vals,data_out["data"][key],label="Despiked Data")
		plt.legend()
	plt.show()

if run_replace is True:
	t_st = time.time()
	options = {"value":100.0}	# Provide value to be replaced
	data3 = {"data":{"series1":[22.2,22.9,31.3,100.0,19.0,100.0]},"time":{"series1":
			['2016-05-09T20:03:04Z','2016-05-09T20:13:04Z','2016-05-09T20:23:04Z','2016-05-09T20:33:04Z',
			 '2016-05-09T20:43:04Z','2016-05-09T20:53:04Z']}}
	lrner = signalProcess(data3,options)
	data_out = lrner.replaceNullData()
	t_en = time.time()
	print "Processing Time: ",t_en - t_st," secs\n"

	# plot before and after
	datetime_vals = [datetime.fromtimestamp(int(it)) for it in data_out["time"]["series1"]]
	for key in data_out["data"]:
		plt.hold(True)
		plt.plot(datetime_vals,data3["data"][key],label="Original Data")
		plt.plot(datetime_vals,data_out["data"][key],label="Replaced Data")
		plt.legend()
	plt.show()
