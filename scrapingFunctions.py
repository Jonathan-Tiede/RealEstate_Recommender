def siteType(tag):
    # So far I have found two versions of the main content section of the home details urls. This will account for both of them.
    try:
        details = tag.find('div',{'class':'layout-content-container'})
        errorCheck = details.find_all('dt')[0].text
        print('Site type 1111 found.')
    except AttributeError:
        details = tag.find('div',{'class':'data-column-container'})
        errorCheck = details.find_all('dt')[0].text
        print('Site type 2 found.')
    except:
        print('Incompatible Site Tag.')
        return
    
    print('Entering daysOnZillow()')
    days = daysOnZillow(details)
    print('Exiting daysOnZillow()')
    print('Entering zillowExtraData()')
    extra = zillowExtraData(details)
    print('Exiting zillowExtraData()')

    output = [days, extra]
    return output

def daysOnZillow(tag):
    '''
    Need to be careful here as well. Some homes haven't been built yet and so there are no "days" on zillow yet. Instead, this
    scraper will pull the number of views and will not add a unit to the end. Ie. "442" instead of "442" views or "442 days."
    '''
    try:
        days = tag.find('dl',{'class':'hdp__sc-ky7q3p-0 dfePgr'})
        days = days.find_all('dt')[0].text
        print('Tag type 1 found.')
        return days
    except AttributeError:
        print('error 1')
        days = 'ERROR'
    try:
        days = tag.find('dl',{'class':'OverviewStatsComponentsstyles__StyledOverviewStats-sc-1bg6b6d-0 nnBbc'})
        days = days.find_all('dt')[0].text
        print('Tag type 2 found.')
        return days
    except AttributeError:
        print('error 2')
        days = 'ERROR'
    try:
        days = tag.find('dl',{'class':'OverviewStatsComponents__StyledOverviewStats-sc-7d6bsa-0 bOcuTH'})
        days = days.find_all('dt')[0].text
        print('Tag type 3 found.')
        return days
    except AttributeError:
        print('error 3')
        days = 'ERROR'
    
    return days

def zillowExtraData(tag):
    try:
        print('test check')
        age = tag.find_all('span',{'class':'Text-c11n-8-84-3__sc-aiai24-0 hdp__sc-6k0go5-3 hrfydd llcOCk'})[0].text
        land = tag.find('span',{'class':'Text-c11n-8-84-3__sc-aiai24-0 hdp__sc-6k0go5-3 hrfydd llcOCk'})[1].text
        print(age)
        print(land)
        data = [age, land]
        return data
    except AttributeError:
        print('Error 1')
        data = ['ERROR', 'ERROR']

    try:
        age = tag.find_all('span',{'class':'Text-c11n-8-84-3__sc-aiai24-0 styles__StyledFactValue-sc-6k0go5-3 hrfydd PeHnt'})[0].text
        land = tag.find('span',{'class':'Text-c11n-8-84-3__sc-aiai24-0 styles__StyledFactValue-sc-6k0go5-3 hrfydd PeHnt'})[1].text
        print(age)
        print(land)
        data = [age, land]
        return data
    except AttributeError:
        print('Error 2')
        data = ['ERROR', 'ERROR']
    
    return data
