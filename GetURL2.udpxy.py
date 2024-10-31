import json, argparse, sys, os, textwrap, re

def SortResult(sourceFile, outFile, urlType, subType):
    f = open(sourceFile, 'r')
    f2 = open(outFile, 'w')
    f2.write('#EXTM3U name="CMCC-IPTV"' + '\n')
    f2.close()
    urlDict = json.loads(f.read())
    channelList = urlDict['channels']
    for channelDict in channelList:
      if re.search('CTV.*清', channelDict['title']) :
        continue
      phychannelsList = channelDict['phychannels']
      if phychannelsList[0].__contains__('params'):
        for phychannelDict in phychannelsList:
          subChannelDict = phychannelDict['params']
          urlResult = SortIPTVSubChannel(subChannelDict,urlType=urlType)
          if urlResult != 'none' and channelDict['subTitle'] !='' :
            writeResult2(outFile,subTitle=channelDict['subTitle'],urlResult=urlResult,channelDict=channelDict, phychannelDict=phychannelDict, subType=subType)
      else:
        subChannelDict = channelDict['params']
        urlResult = SortIPTVSubChannel(subChannelDict,urlType=urlType)
        if urlResult != 'none' and channelDict['subTitle'] !='' :
            #writeResult(outFile,subTitle=channelDict['subTitle'],urlResult=urlResult,channelDict=channelDict)
            writeResult2(outFile,subTitle=channelDict['subTitle'],urlResult=urlResult,channelDict=channelDict, phychannelDict=None, subType=subType)

    '''
    for channelDict in channelList:
        for channelDictKey,channelDictValue in channelDict.items():
            if channelDictKey == 'params':
                subChannelDict = channelDict[channelDictKey]
                urlResult = SortIPTVSubChannel(subChannelDict,urlType=urlType)
                if urlResult != 'none' and channelDict['subTitle'] !='' :
                    writeResult(outFile,subTitle=channelDict['subTitle'],urlResult=urlResult,channelDict=channelDict)
    '''
    f.close()

def SortIPTVSubChannel(subChannelDict,urlType):
    url = ''
    if subChannelDict[urlType] != '' :
        url = subChannelDict[urlType]
    else:
        url = 'none'
    return url

def writeResult(outFile,subTitle,urlResult,channelDict):
    f2 = open(outFile, 'a')
    subTitle = '#EXTINF:-1' + ' tvg-logo="' + re.sub('([0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{1,5}','192.168.6.249',channelDict['icon']) + '",' + channelDict['subTitle']
    #subTitle = '#EXTINF:-1' + ' tvg-logo="' + channelDict['icon'] + '",' + channelDict['subTitle']
    f2.write(subTitle + '\n')
    f2.write('http://192.168.6.1:4022/udp/' + urlResult.strip('rtp://|udp://') + '\n')
    #f2.write(urlResult + '\n')
    f2.close()

def writeResult2(outFile,subTitle,urlResult,channelDict,phychannelDict, subType):
    f2 = open(outFile, 'a')
    grouptitle = ''
    if re.search('CCTV', channelDict['subTitle']) :
      grouptitle = ' group-title="CCTV" '
    elif re.search('卫视', channelDict['subTitle']) :
      grouptitle = ' group-title="卫视" '
    else :
      grouptitle = ''
    subTitle = '#EXTINF:-1'
    if subType == 'udpxy' :
      subTitle = subTitle + ' tvg-logo="' + re.sub('([0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{1,5}','192.168.6.249',channelDict['icon']) + '"'
    else :
      subTitle = subTitle + ' tvg-logo="' + channelDict['icon'] + '"'

    subTitle = subTitle + grouptitle + ',' + channelDict['subTitle']
    if phychannelDict != None :
      if re.search('清', phychannelDict['bitrateTypeName']) :
        subTitle = re.sub('.清$', '', subTitle)
      subTitle = subTitle + '-' + phychannelDict['bitrateTypeName']
    f2.write(subTitle + '\n')
    if subType == 'udpxy' :
      f2.write('http://192.168.6.1:4022/udp/' + urlResult.strip('rtp://|udp://') + '\n')
    else :
      f2.write(urlResult + '\n')
    f2.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help = True
            , description = "This is a script use to convert CMCC-IPTV official live sources "
                            "format to udpxy format. \n"
                            "Example: python3 GetURL.py -f getAllChannel.json -t zteurl -s udpxy -o iptv.m3u"
            , formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-f', '--file', action='store', help='Specify IPTV-sources file.')
    parser.add_argument('-t', '--type', action='store', help='Specify IPTV channel, hwurl is for HUAWEI url, zteurl is for ZTE url')
    parser.add_argument('-s', '--subtype', action='store', help='Specify output for udpxy or not')
    parser.add_argument('-o', '--outfile', action='store', help='Specify output file name you want to save.')

    if len(sys.argv) == 1:
        print(parser.print_help())
        sys.exit(1)

    options = parser.parse_args()

    if os.path.exists(options.file) == False:
        print("[-] File not existed, maybe you got a typo!")
    elif options.type not in ['hwurl','zteurl']:
        print("[-] Wrong type!")
    else:
        SortResult(sourceFile=options.file, urlType=options.type, subType=options.subtype, outFile=options.outfile)
        print("[+] Convert finished!")

