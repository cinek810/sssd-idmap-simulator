#!/usr/bin/python3

import matplotlib.pyplot as plt
import random
import mmh3
uid_range_min=2000
uid_range_max=3000
range_size=150


domains={
		"dom2": { "min_rid": 100, "max_rid": 200},
		"dom1": { "min_rid": 100, "max_rid": 300, "domSid": "2999047449-515994586-265227950"}, 
		"dom3": { "min_rid": 100, "max_rid": 200}
	}

domains={
		'dom1': {'domSid': '2999047449-515994586-265227950', 'max_rid': 300, 'min_rid': 100}, 
		'dom3': {'domSid': '568219641-871961618-465585696', 'max_rid': 200, 'min_rid': 100}, 
		'dom2': {'domSid': '496581681-170580794-283878795', 'max_rid': 200, 'min_rid': 100}
	}

#domains={
#		'dom1': {'domSid': '2999047449-515994586-265227250', 'max_rid': 300, 'min_rid': 100}, 
#		'dom3': {'domSid': '568219641-871961618-465585696', 'max_rid': 200, 'min_rid': 100}, 
#		'dom2': {'domSid': '496581681-170580794-283878795', 'max_rid': 200, 'min_rid': 100}
#	}


for dom_name,dom_attr in domains.items():
	try:
		dom_attr["domSid"]
	except KeyError:
		rand1=random.randrange(100000000,999999999)
		rand2=random.randrange(100000000,999999999)
		rand3=random.randrange(100000000,999999999)
		domains[dom_name]["domSid"]=str(rand1)+"-"+str(rand2)+"-"+str(rand3)
	

collProb={}
for range_size in [100]:

	nr_ranges=int((uid_range_max-uid_range_min)/range_size)
	print("Number of ranges="+str(nr_ranges)+" range_size="+str(range_size))
	
	slices={}
	tries=0
	collisions={0: 0, 1: 0,2: 0, 3: 0, 4: 0}
	errors=0
	oldColl=20
	newColl=10
	eps=0.001

	for i in range(1,8000):
		dom_attr=list(domains.values())[random.randrange(0,len(domains.values()))]
		myRid=random.randrange(dom_attr["min_rid"],dom_attr["max_rid"])
		tries=tries+1
		firstRid=int(myRid/range_size)*range_size
		sliceName="S-1-5-21-"+dom_attr["domSid"]+"-"+str(firstRid)
		sliceNumber=mmh3.hash(sliceName)%nr_ranges;
		print("\tdomSid="+dom_attr["domSid"]+" myRid="+str(myRid)+" firstRid="+str(firstRid)+" sliceNumber="+str(sliceNumber))
		try:
			if(slices[sliceName]==sliceNumber):
				print("\t\t\tSlice already alocated in \"primary\" location")
				collisions[0]+=1
			else:
				col_order=abs(sliceNumber-slices[sliceName])%nr_ranges
				print("\t\t\tslice already allocated but it's a collision of "+str(col_order)+" order. Use: "+str(slices[sliceName])+" primary is "+str(sliceNumber))
				try:
					collisions[col_order]+=1
				except KeyError:
					collisions[col_order]=1
		except KeyError:
			print("\t\tWe have to find new slice, slices in use:")
			print("\t\t"+str(slices.values()))
			colNum=0
			weHadError=False
			while(len(slices)<nr_ranges):
				try: 
					usedFor=list(slices.keys())[list(slices.values()).index(sliceNumber)]
					print("\t\t\tSlice "+str(sliceNumber)+" already in use")
				except ValueError:
					print("\t\t\tNot used, we can allocate this slice, sliceNumber="+str(sliceNumber)+", order = "+str(colNum))
					slices[sliceName]=sliceNumber
					break;
				#break didn't happen so we have another collision
				colNum+=1
				if sliceNumber<nr_ranges-1:
					sliceNumber=sliceNumber+1
					print("\t\t\t\tTrying next slice")
				else:
					sliceNumber=0;
					print("\t\t\t\tChecking from zero")

			else:
				errors=errors+1
				print("\t\t\tOut of ranges");
				weHadError=True
			if weHadError == False:
				try:
					collisions[colNum]+=1
				except KeyError:
					collisions[colNum]=1

		print("\terrors="+str(errors)+" collisions="+str(collisions)+" tries="+str(tries))
	
	collProb[range_size]={"nr_ranges": nr_ranges, "collProb": collisions, "errors": errors, "tries": tries, "range_size": range_size}
				
#	print("oldColl="+str(oldColl)+"newColl="+str(newColl))

range_size,attrs=zip(*sorted(collProb.items()))
from numpy import array
range_size=array(range_size)
import pprint

pp=pprint.PrettyPrinter(indent=4)
pp.pprint(attrs)

ax = plt.subplot(111)
w=1
ax2=ax.twinx()
ax2.set_ylabel("Number of ranges - green  bar")
ax.set_ylabel("Probability - collision(blue), error(red)")
ax2.bar(range_size-3*w, [ myAttrs["nr_ranges"] for myAttrs in attrs],w,color='g', align='center')
ax.bar(range_size-2*w, [ myAttrs["collProb"][1]/myAttrs["tries"] for myAttrs in attrs],w,color='b', align='center')
ax.bar(range_size-w, [ myAttrs["collProb"][2]/myAttrs["tries"] for myAttrs in attrs],w,color='y', align='center')
ax.bar(range_size, [ myAttrs["collProb"][3]/myAttrs["tries"] for myAttrs in attrs],w,color='coral', align='center')
ax.bar(range_size+w, [ myAttrs["collProb"][4]/myAttrs["tries"] for myAttrs in attrs],w,color='black', align='center')
ax.bar(range_size+2*w, [ myAttrs["errors"]/myAttrs["tries"] for myAttrs in attrs],w,color='r', align='center')
#ax.bar(x-w,collisions[1],color='r', align='center')
ax.set_xticks(range_size)
ax.set_xticklabels(range_size)
plt.text(0,-7,"Tested with: "+str(domains),wrap=True)
#ax.autoscale(tight=True)
plt.show()

print(domains)
