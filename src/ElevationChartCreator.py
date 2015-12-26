# Copyright Google Inc. 2010 All Rights Reserved
import simplejson
import urllib
import googlemaps

ELEVATION_BASE_URL = 'http://maps.google.com/maps/api/elevation/json'
CHART_BASE_URL = 'http://chart.googleapis.com/chart'

def getChart(chartData, chartDataScaling="20,60", chartType="lc",chartLabel="Elevation in Meters",chartSize="500x160", chartColor="orange", **chart_args):
    chartDataScaling = "%d,%d" %(min(chartData), max(chartData))
    
    chart_args.update({
        'cht': chartType,
        'chs': chartSize,
        'chl': chartLabel,
        'chco': chartColor,
        'chds': chartDataScaling,
        'chxt': 'x,y',
        'chxr': '1,' + chartDataScaling
    })

    dataString = 't:' + ','.join(str(x) for x in chartData)
    chart_args['chd'] = dataString.strip(',')

    chartUrl = CHART_BASE_URL + '?' + urllib.urlencode(chart_args)

    print("")
    print("Elevation Chart URL:")
    print("")
    print chartUrl

ddd = 0
def getElevation(path="",samples="100", distance=0, sensor="false", **elvtn_args):
    elvtn_args.update({
        'path': path,
        'samples': samples,
        'sensor': sensor
    })

    url = ELEVATION_BASE_URL + '?' + urllib.urlencode(elvtn_args)
    content = urllib.urlopen(url).read()
#     print content
    response = simplejson.loads(content)
    # Create a dictionary for each results[] object
    elevationArray = []

    locations = []
    for resultset in response['results']:
      elevationArray.append(resultset['elevation'])
      locations.append(resultset['location'])

#     for i in range(len(locations)-1):
#         u, v = locations[i], locations[i+1]
#         distance = ((u["lat"]-v["lat"])**2 + (u["lng"]-v["lng"])**2) ** 0.5
#         print distance    
    
    sections = []
    for i in range(len(elevationArray)-1):
        sections.append((distance, elevationArray[i+1]-elevationArray[i]))
    return sections

# Create the chart passing the array of elevation data
#     getChart(chartData=elevationArray)   

if __name__ == '__main__':
    
    l = [(526, "mursE}izyXMcAISIMIGMGEAK?O@OLEF?BEHa@xBINCBG@QCGGEGEME_A@UBSH]N_@Pa@DW?K@WAa@AWOs@Mg@o@sBIEOKu@SMC"),
         (1061, "_`ssE{zzyXYGECGCEGCQ?G?IBG\[HMBE@K?MCQISSWGIIEOGKCO?S@w@Rk@T{@X]BS?UCGAECCEEGAKAQBKHWJUR[NMFC|@_@FCHKDKBK?G?MEOCCIIOCe@Ck@?{AA[@SBIHc@n@q@|AI^AJAJ?J@HDJBLl@hAf@bAx@fB^bBBV?PADCLUr@a@|@MLMD"),
         (2628, "aossEyozyXA?OCCSHUROJIHMDKJYBS?SCUI[Oc@Q]_@k@gAwAaAmAQIKGCIAE@u@AGGQGGIEeBa@KECGIWEGGIICK?CD}AtAEBI@I@cBFG?WISAwCEm@@o@BWBYDgBc@KEGEAASg@GGIGIAU?MD[Je@NYJU@GAECW_@KKCASAKAIECASWGGKAI?c@FM?EAEIEKSgACKGEKAE?IBWJE@G@MCWKIAG@IBEDGFCJAB?JDLXp@AJy@d@C@CDELAJ@B@DFFLHnBl@`@TNJDFFH?JCDGJaAp@EHWb@GFUTG@IBkARY@S?EAMEw@m@KCKEG?MDKBOJUPOHGBI?SEG?YDK?ICEEIGEIAIAICc@CUAIEMGSqAoBOQYWIBSR?BRfAN`A?JAJELGDMDk@ROHEFCH?LF\BN?PANATELEJWb@IJ{@h@EJo@fBALANAbACJEFIDK?MEs@QQCM?SBaAVE?G?_@e@GC"),
         (2328, "efvsEiozyXS?e@@M?c@K{@Wg@c@OKQGK?I@KFQTw@bBGVGj@Ah@B|@ARARCXW`AUt@GPOPUNM@Q?KAKCGIOQw@qBg@gAc@mAQi@AO?MDEFEFCx@GFCDCFGBK@IAQKcAEIEGGEq@a@CECEIWYgB?K@GDQFEFEpAc@HGBE@I?MCIWk@c@qCQm@K_@CU?c@@OD]DOHUNOPO~@SHEHEBI@E@MCMAEm@cAGWGk@AEGEQKOIMM_@m@Q[[iACMGGKGMEIAQ?c@BQ?UYa@c@KS]qA_@y@a@wBAI?g@ZkDB]?SEOKGSMQKUUy@cA[i@u@kAEIY}AY{AIcACIi@iAIS_@sBGWMQ_@S"),
         (982, "yrwsEyc}yXu@a@OCK?QBI@SLWNIBK?ICIEEGaAsA[_@MMKEKEOEs@KUEi@Um@_AMSKKsAu@MKIMKMyAkCKMIGGGWKSQIGCGEKGa@G]CYAMA}AA]Em@Qo@COG[AU?QBO^{A@KRyBHq@FiAAOCKQc@")]

    # Collect the Latitude/Longitude input string
    # from the user
    sections = []
    for v in l:
        polyline = googlemaps.convert.decode_polyline(v[1])
        for i in range(0, len(polyline), 80):
            paths = []
            for point in polyline[max(0, i-1):min(i+80, len(polyline))]:
                paths.append(str(point["lat"]) + "," + str(point["lng"]))
            path = "|".join(paths)
            sections += getElevation(path, str(len(paths)-1), float(v[0])/(len(polyline)-1))
    
    sections2 = []
    distance = 0
    height = 0
    
    for i, section in enumerate(sections):
        ap = int(distance/100) < int((distance+section[0])/100)
        if ap:
            rest = distance+section[0] - int(distance/100)*100
            sections2.append((int(distance/100)*100, height + section[1] * ((section[0]-rest)/distance)))
        
        distance += section[0]
        height += section[1]
    
    for i in range(len(sections2)):
        print sections2[i][1] - (0 if i==0 else sections2[i-1][1])
        