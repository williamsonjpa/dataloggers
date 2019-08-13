import os

import ntpath
import glob


def run_conversion2_script(root, setup, collection):
    in_directory = root + '/Data/Raw'
    out_folder = root + '/Data/Converted'

    #clear directories where there are outputs
    clear_directory(out_folder, '.csv')

    iterate_convert_txt_to_non_ascii(root, in_directory, out_folder, root + setup, root + collection)        


def clear_directory(directory, extension):
    '''
    clears a directory and subdirectories of files with the extension provided e.g. '.txt'
    '''
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            if name.lower().endswith(extension):
                os.remove(os.path.join(dirpath, name))

def iterate_convert_txt_to_non_ascii(root, in_directory, out_folder, setup, collection):

    #convert the setup and collection files
    convert_txt_to_ascii(setup, root + '/Data/Final')
    convert_txt_to_ascii(collection, root + '/Data/Final')

    #generate variables to track how many files have been converted
    infile_length = 0
    filenumber = 0

    #run a loop counting the number of files to be processed for infile_length
    for dirpath, dirnames, files in os.walk(in_directory):
        for name in files:
            if name.lower().endswith('.txt'):
                infile_length += 1

    #run a loop converting the files and tracking which number file it is processing
    for dirpath, dirnames, files in os.walk(in_directory):
        for name in files:
            if name.lower().endswith('.txt'):
                convert_txt_to_ascii(os.path.join(dirpath, name), out_folder)
                filenumber += 1

                #print number of files converted 
                if str(filenumber)[-1] == '0' or filenumber == infile_length:
                    print('Converted ' + str(filenumber) + ' of ' + str(infile_length) + ' files!')

def convert_txt_to_ascii(inputfile ,outfolder):
    '''
    converts the files put in to files without nonascii characters in 
    '''
    #define what non ascii characters are
    nonascii = bytearray(range(0x80, 0x100))

    #get the filename without the path
    filenamenopath = ntpath.basename(inputfile)
    

    #fix any SJI files that have a ' ' in the name instead of a hyphen
    ###check that this works....
    if filenamenopath[10] == ' 'and filenamenopath[-3:] == 'txt':
        startfile = filenamenopath[:10]
        endfile = filenamenopath[11:]
        filenamenopath = startfile + '-' + endfile

    #change the extenson to csv
    filenamenopath = filenamenopath[:-3]
    filenamenopath = filenamenopath + 'csv'

    #get rid of nonascii characters and resave the file
    with open(inputfile,'rb') as infile, open(outfolder + '/' + filenamenopath,'wb') as outfile:
        for line in infile: # b'\n'-separated lines (Linux, OSX, Windows)
            outfile.write(line.translate(None, nonascii))
