from pathlib import Path
import json
import os
import requests


class FileManager:

    '''
    This class has methods for converting files to python usable objects and back. The url list is kept in a text file
    delimited by line breaks for human legibility. The spirit dataclass objects are converted to dictionaries and saved as 
    as json files. 
    '''

    # Take a list variable and a name for the file and create/overwrite the file then add contents as a list with line breaks
    def output_list_to_text_file(url_list, directory_filepath):

        '''
        This method outputs a python list to a line break delimited text file to a folder designated by the mainpage url
        -
        Arguments:
            url_list (list): List of of spirit profile pages
            directory_filepath (string): Filepath for the list to be saved. Usually spirit.filepath.
        
        '''

        
        Path(directory_filepath).mkdir(parents=True, exist_ok=True)
        
        with open(f'{directory_filepath}/url_list.text', 'w') as outfile:
            pass

        with open(f'{directory_filepath}/url_list.text', 'a') as outfile:
            for url in url_list:
                outfile.write(url)
                if not url == url_list[-1]:
                    outfile.write('\n')

    
    def output_spirit_to_data_file(spirit):
        
        '''
        Method that takes an input (dataclass instance) and the directory filepath (spirit.filepath) and outputs the attributes of the input
        as a dictionary in a json file. The attribute spirit.filepath of the input are used to name the folders where the final data.json file is saved.
        -
        eg. The Whisky Exchange / Single Malt Scotch Whisky / Region / Brand name / product name / data.json'

        Arguments:
            input (dataclass instance):
        
        '''
               
        Path(spirit.filepath).mkdir(parents=True, exist_ok=True)
               
        # json data file
        json_path = f'{spirit.filepath}/data.json'

        inputdict = spirit.__dict__
        with open(json_path, 'w') as outfile:
            json.dump(inputdict, outfile, indent=4)
        
        # jpg image file
        image_path = f'{spirit.filepath}/{spirit.name}.jpg'
        
        try:
            r = requests.get(spirit.image_url)
            with open(image_path, 'wb') as outfile:
                outfile.write(r.content)
        except AttributeError: # due to issue fetching url for jpg
            pass

        return json_path, image_path
           
         
    def unpack_text_to_python_list(file_path):

        '''
        Method to convert the contents of a line break separated text file at 'file path' to a Python List.
        -
        Arguments:
            file_path (string): path to the file to be read as a string
            
        Returns:
            url_list (list): a list of urls to be scraped
        '''

        with open(file_path, 'r') as outfile:
            url_list_content = outfile.read()
            url_list = url_list_content.split('\n')
            
        return url_list

   
    def unpack_json_file(json_file_path):

        '''
        Method to convert the contents of a json file dictionary to a python dictionary
        -
        Arguments:
            json_file_path (string): the path of the json file to be converted
            
        Returns:
            spirit_data_dict (dict): a dictionary of the contents of the json file
        '''

        try:
            with open(json_file_path) as f:
                try:
                    return json.load(f)
                except ValueError:
                    raise ValueError('{} is not valid JSON.'.format(json_file_path))
        except IOError:
            raise IOError('{} does not exist.'.format(json_file_path))
        