def daysOnZillow(tag):
    # Need to be careful here as well. Some homes haven't been built yet and so there are no "days" on zillow yet. Instead, this scraper will
    # pull the number of views and will not add a unit to the end. Ie. "442" instead of "442" views or "442 days."
    try:
        days = tag.find('dl',{'class':'hdp__sc-ky7q3p-0 dfePgr'})
        days = days.find_all('dt')[0].text
        print('Tag type 1 found.')
        return days
    except:
        print('error 1')
        days = 'ERROR'
    try:
        days = tag.find('dl',{'class':'OverviewStatsComponentsstyles__StyledOverviewStats-sc-1bg6b6d-0 nnBbc'})
        days = days.find_all('dt')[0].text
        print('Tag type 2 found.')
        return days
    except:
        print('error 2')
        days = 'ERROR'
    try:
        days = tag.find('dl',{'class':'OverviewStatsComponents__StyledOverviewStats-sc-7d6bsa-0 bOcuTH'})
        days = days.find_all('dt')[0].text
        print('Tag type 3 found.')
        return days
    except:
        print('error 3')
        days = 'ERROR'
    
    return days

def siteType(tag):
    # So far I have found two versions of the main content section of the home details urls. This will account for both of them.
    try:
        details = tag.find('div',{'class':'layout-content-container'})
        errorCheck = details.find_all('dt')[0].text
        print('Site type 1 found.')
    except AttributeError:
        details = tag.find('div',{'class':'data-column-container'})
        errorCheck = details.find_all('dt')[0].text
        print('Site type 2 found.')
    except:
        print('Incompatible Site Tag.')
        return
        
    days = daysOnZillow(details)
    return days