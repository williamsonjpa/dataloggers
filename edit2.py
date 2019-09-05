import os

import glob
import os.path
import pandas as pd
import numpy as np

def iterate_edit2(root,setup,collection):
    '''
    iterate edit2 script over files in added info directory
    '''

    ###clear out the folder where the edited files are going to be produced
    clear_directory(root + '/Data/Edited','.csv')

    #clear out the folder where broken files are moved
    clear_directory(root + '/Data/ProblemFiles','.csv')

    #create a fail_list for recording failures
    fail_list = ['fail','list']

    infilelist = glob.glob(os.path.join(root + '/Data/AddedInfo', "*.csv"))
    filenumber = 0

    for f in infilelist:
        fail_list = remove_useless_data(root, \
            f, \
            root + '/Data/Final' + setup, \
            root + '/Data/Final' +collection, \
            fail_list)
        filenumber += 1
        infile_length = len(infilelist)

        #only prints the progess message every 10th file or for the last file
        if str(filenumber)[-1] == '0' or filenumber == infile_length:
            print('Edited ' + str(filenumber) + ' of ' + str(infile_length) + ' files!')

    #print a list of failures at the end
    print('There were failures in ' + str(len(fail_list) - 2) + ' out of ' + \
        str(infile_length) + ' files. These files have been moved to the Data/ProblemFiles directory.')



def remove_useless_data(root,infile,setup,collection,fail_list):
    '''
    A function to edit the datalogger files that have already had info added and been
    converted to ASCII characters only.
    Start and end datetimes are read from the setup and collecion files so that
    we can make sure we only use data from when the logger was in position.
    Failed dataloggers are moved to folders that are sorted by the problems that
    caused failure, e.g. failure to match to datasets, no recorded data within datetime
    window...
    Number of days of recording is appended to each datalogger column.
    '''
    #read in file
    df = pd.read_csv(infile)

    #strip out useful information to check if the file matches to set up and collection data
    river = df.loc[0,'River']
    loggerID = df.loc[0,'loggerID']
    position = df.loc[0,'Position']
    point = df.loc[0,'Point']


    #generate a datetime from setup data
    startDateTime = generate_setup_date_time(setup,infile,river,loggerID,position,point)

    #generate a datetime from collection data
    endDateTime = generate_collection_date_time(collection,infile,river,loggerID,position,point)

    #checks that the previous functions succesfully generated date times, moves problem files
    error_result = check_for_date_time_errors(root,startDateTime,endDateTime,infile,df)

    #processes cutoff times by running them through the document
    (df,error_result) = process_cut_off_times(root,df,startDateTime,endDateTime,infile,error_result)

    #add failed files to a list of failed files to print at the end
    if error_result == 'BATTERY' or error_result == 'FAILED':
        fail_list = process_date_time_errors(fail_list,infile)

    #calculate number of days recording for and append to the dataframe
    df = calculate_days_in_field(df)
    df = df.loc[:,'Time':]

    outfile = generate_infile_name(infile)

    #save the file to the AddedInfo folder
    if error_result == 'PASSED':
        df.to_csv(root + '/Data/Edited/' + outfile)


    return fail_list

def clear_directory(directory,extension):
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            if name.lower().endswith(extension):
                os.remove(os.path.join(dirpath, name))

def generate_setup_date_time(setup,infile,river,loggerID,position,point):
    '''
    Generate a datetime (date, time) to cut off the excess recordings at the start
    '''
    df_s = pd.read_csv(setup)
    duplicateError = 0

    for i in df_s.index:
        splitData = df_s.loc[i,'GPS point name'].split('-')
        df_s.loc[i,'point'] = splitData[1]

    #matches infile to the setup file
    for i in df_s.index:
        # print( '[1]'+str(df_s.loc[i,'Site']).lower()+str(river).lower() +
        # '[2]'+str(df_s.loc[i,'point'])+str(point)+
        # '[3]'+str(df_s.loc[i,'Data logger ID#'][-3:])+str(loggerID)+
        # '[4]'+df_s.loc[i,'Data logger point'].lower().replace(" ", "")+position.lower())
        if str(df_s.loc[i,'Site']).lower() == str(river).lower() and \
        str(df_s.loc[i,'point']) == str(point) and \
        str(df_s.loc[i,'Data logger ID#'][-3:]) == ('00' + str(loggerID))[-3:]  and \
        df_s.loc[i,'Data logger point'].lower().replace(" ", "") == position.lower():
            date = df_s.loc[i,'Date']
            time = df_s.loc[i,'Time put out']
            if np.isnan(df_s.loc[i,'Coordinate- E']) != True:
                long = df_s.loc[i,'Coordinate- E']
            else:
                long='NA'
            if np.isnan(df_s.loc[i,'Coordinate- N']) != True:
                lat = df_s.loc[i,'Coordinate- N']
            else:
                lat='NA'
            duplicateError += 1

    #check there has only been one match
    if duplicateError > 1:
        date = 'MULTIPLEMATCHES'
        time = 'MULTIPLEMATCHES'
        long='NA'
        lat='NA'
    elif duplicateError == 0:
        date = 'NOMATCH'
        time = 'NOMATCH'
        long='NA'
        lat='NA'

    return (date,time,long,lat)

def generate_collection_date_time(collection,infile,river,loggerID,position,point):
    '''
    Generate a datetime (date, time) to cut off the excess recordings at the start
    '''
    df_c = pd.read_csv(collection)
    duplicateError = 0

    #matches infile to the setup file
    for i in df_c.index:
        if str(df_c.loc[i,'Riparian #']).lower() == str(river).lower() and \
        df_c.loc[i,'Vegetation plot #'] == point and \
        str(df_c.loc[i,'Data logger unique ID #'][-3:]) == ('00' + str(loggerID))[-3:] and \
        df_c.loc[i,'Distance point in transect'].lower().replace(" ", "") == position.lower():
            date = df_c.loc[i,'Date']
            time = df_c.loc[i,'Time']
            duplicateError += 1

    #check there has only been one match
    if duplicateError > 1:
        date = 'MULTIPLEMATCHES'
        time = 'MULTIPLEMATCHES'
    elif duplicateError == 0:
        date = 'NOMATCH'
        time = 'NOMATCH'

    return (date,time)

def check_for_date_time_errors(root,startDateTime,endDateTime,infile,df):

    if 'NOMATCH' in startDateTime:
        df.to_csv(root + '/Data/ProblemFiles/SetupNoMatchErrors/' + infile.split('/')[-1])
        return 'FAILED'

    elif 'MULTIPLEMATCHES' in startDateTime:
        df.to_csv(root + '/Data/ProblemFiles/SetupDuplicateMatchErrors/' + infile.split('/')[-1])
        return 'FAILED'

    elif 'MULTIPLEMATCHES' in startDateTime:
        df.to_csv(root + '/Data/ProblemFiles/CollectionDuplicateMatchErrors/' + infile.split('/')[-1])
        return 'FAILED'

    elif 'NOMATCH' in endDateTime:
        df.to_csv(root + '/Data/ProblemFiles/CollectionNoMatchErrors/' + infile.split('/')[-1])
        return 'FAILED'

    else:
        return 'PASSED'

def process_date_time_errors(fail_list,infile):
    '''
    returns a fail_list with the failed file appended to the end of it

    '''
    fail_list.append(infile.split('/')[-1])
    return fail_list

def process_cut_off_times(root,df,startDateTime,endDateTime,infile,error_result):

    if error_result == 'PASSED':
        #if the error check is passed then procced to cutting off the extra start and end datetimes
        (df,error_result) = cut_off_start_date_time(df,startDateTime,error_result)
        #if there has  not been a battery fail before the logger was set up
        if error_result == 'PASSED':
            df = cut_off_end_date_time(df,endDateTime)
        #if there has been a battery error stick it in the battery folder
        elif error_result == 'BATTERY':
            df.to_csv(root + '/Data/ProblemFiles/BatteryErrors/' + infile.split('/')[-1])


    elif error_result == 'FAILED':
        pass

    #raise an error if none of these error_result matches are true
    else:
        raise ValueError('Failed to generate an error result from check_for_date_time_errors().')

    return (df,error_result)

def cut_off_start_date_time(df,startDateTime,error_result):
    '''
    returns a dataframe (df) where the all times before 12:00pm after the set up date time
    have been deleted
    '''
    #varaibles to check if the date and time have already been found in the dataframe
    date_found = 0
    time_found = 0
    df.loc[:,'long'] = startDateTime[2]
    df.loc[:,'lat'] = startDateTime[3]
    df.loc[:,'setup_date'] = startDateTime[0]


    for i in df.index:
        #if the date has not yet been found
        if date_found==0:
            #if date row matches the start date
            if pd.to_datetime(df.loc[i,'Date'])==pd.to_datetime(startDateTime[0]):
                date_found=1

            #once the date is found we need to look for the next time recording on the hour after the setup
        elif date_found==1 and time_found==0:
            if int(df.loc[i,'Time'][:2])>int(startDateTime[1][:2]):
                time_found=1
                df=df[df.index>=i]


        else:
            pass

    #if the logger failed before it was deployed (here called a battery error) change the error_result to 'BATTERY'
    if date_found==0:
        #if the datalogger started recording after it was put out
        if pd.to_datetime(df['Date'].iloc[0])>pd.to_datetime(startDateTime[0]):
            pass
        #otherwise it must be a battery failing before it recorded
        else:
            error_result='BATTERY'

    return (df,error_result)

def cut_off_end_date_time(df,endDateTime):
    '''
    looks for the datalog after which the logger was collected and then cuts off the df from there onwards
    '''

    date_found=0
    time_found=0

    for i in df.index:
        #if the date has not yet been found
        if date_found==0:
            #if date row matches the start date
            if df.loc[i,'Date'][:10]==endDateTime[0]:
                date_found=1

        #now look for the time after the recorder was collected, if it is not found, the dataframe is not altered
        elif date_found==1 and time_found==0:
            if int(df.loc[i,'Time'][:2])>int(endDateTime[1][:2]):
                time_found=1
                df=df[df.index<i]


    return df




def calculate_days_in_field(df):
    '''
    calculates a column of the total number of days the logger was in the field for
    (day when logger stopped recording - setup day) (column called 'days_recorded')
    '''
    ##convert to datetime format (may need to be fixed, date is in DD/MM/YYYY format)
    df['DateTime'] = pd.to_datetime(df['Date'])
    # create the new column by subtracting start date from last date on df
    df['days_recorded']=str(df['DateTime'].iloc[len(df['DateTime'])-1]-df['DateTime'].iloc[0]).split(' ')[0]

    return df


def generate_infile_name(infile):
    filename=infile.split('/')[-1]
    return filename
