import re

# Use regular expressions to extract the relevant information
file = open('text/interruptions_20230420.txt', 'r')
text = file.read()

areas = re.findall(r"AREA: +(?P<area>.*)", text)
dates = re.findall(r"DATE: +\w+ (\d{2}.\d{2}. ?\d{4})", text)
times = re.findall("\s?TIME:{0,} (\d{1,}.\d{2} A.M.) [-–] (\d{1,}.\d{2} P.M.)", text)
locations = re.findall(r"[P].M.\s+([\w\s,&/.'’-]+)&\s*adjacent\s*customers", text)

interruptions = []

# TODO: If areas list doesn't have the same no. of elements as the date & time, raise an error
if len(areas) == len(dates) == len(times) == len(locations):
    for i in range(len(areas)):
        interruptions.append({
            "area": areas[i],
            "date": dates[i],
            "time": times[i],
            "locations": locations[i]
        })



for i in interruptions:
    print(i)

file.close()
# Create a list of dictionaries to represent the data
# data = []
# for i in range(len(regions)):
#     data.append({
#         "region": regions[i],
#         "area": areas[i],
#         "date": dates[i],
#         "time": times[i],
#         "locations": locations[i]
#     })

# # Print the data in tabular format
# for datum in data:
#     print(datum)

# file.close()
