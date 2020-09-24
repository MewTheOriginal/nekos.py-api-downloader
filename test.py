#This program is made to download random images infinitely(without repeating) from the nekos.py api.
#It only downloads images in the img function

#needed because it is where the main function is stored
import nekos
#imported so that the image can be downloaded
import requests
#imported to move files and to make folders/files
import os
#imported to store already finished links and banned links
import json

#list of possible args for nekos.img() function
imgs = ['feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo', 'solog', 'feetg', 'cum', 'erokemo', 'les', 'wallpaper', 'lewdk', 'ngif', 'tickle', 'lewd', 'feed', 'gecg', 'eroyuri', 'eron', 'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar', 'gasm', 'poke', 'anal', 'slap', 'hentai', 'avatar', 'erofeet', 'holo', 'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg', 'pwankg', 'classic', 'kuni', 'waifu', 'pat', '8ball', 'kiss', 'femdom', 'neko', 'spank', 'cuddle', 'erok', 'fox_girl', 'boobs', 'Random_hentai_gif', 'smallboobs', 'hug', 'ero', 'smug', 'goose', 'baka', 'woof']

#folder creation
def createFolder(directory):
    try:
        #makes the folder if not in the current folder
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        #passes the OSError
        pass

#creates a folder for each argument if the folder is not already there
for img in imgs:
    createFolder('./{}/'.format(img))

#a variable to set always at true for a forever while loop
check = 'true'

#upon start, downloaded urls are already declared
with open('urls.json', 'r') as f:
    urls = json.load(f)

#upon start, error causing urls are already declared
with open('banned.json', 'r') as f:
    banned = json.load(f)

#forever while loop to repeat the code needed
while check == 'true':
    #for loop to run through all the possible arguments
    for img in imgs:
        #gets a url
        try:
            url = nekos.img(img)
        except:
            #some errors may occur on creation like cannot contact api. This allows the code to skip that section so that it won't cause further errors
            print('An error happened with the neko api')
            continue
        #try funtion in case an error happens
        try:
            #makes the name of the file based on the file name listed in the url (organized like this: url/arg/name)
            name = url.replace("https://cdn.nekos.life/{}/".format(img),"")
            #if the new url is already in the ban list, it skips it to not cause errors
            if url in banned['ban']:
                #prints the url to show you the attempts made
                print('A banned link was attempted to be downloaded ({})'.format(url))
                continue
            #if function to pass the url into the code ONLY IF it is not already downloaded
            if url not in urls['urls']:
                #gets the url's content
                response = requests.get(url)
                #makes the file with the variable name as the name of the file and opens it in write mode(stream). An error may occur if the name is too long
                file = open(name, "wb")
                #writes the content of the url, in this case the gif or the picture
                file.write(response.content)
                #closes the writting stream
                file.close()
                #adds the url to the already downloaded list
                urls['urls'].append(url)
                #saves the list so that if the code is cut off, it can still have a record of the list
                with open('urls.json','w') as f:
                    json.dump(urls, f, indent = 4)
                #moves the file by renaming the path. an error occurs if the path name is too long
                os.rename('{}/{}'.format(os.getcwd(), name), '{}/{}/{}'.format(os.getcwd(), img, name))
                #prints the current amount of files recorded.
                print('Total downloaded images: {} \n   Total Banned Links: {}'.format(len(urls['urls']), len(banned['ban'])))
        except:
            #if an error that is stated above occurs, this code happens
            #if the path name was too long, the url will be saved into the downloaded list so this is to take it back out
            if url in urls['urls']:
                urls['urls'].pop(url)
                with open('urls.json','w') as f:
                    json.dump(urls, f, indent = 4)
            #adds the new link to the error causing link list
            banned['ban'].append(url)
            #saves the ban list
            with open('banned.json','w') as f:
                json.dump(banned, f, indent = 4)
            #tells you the specific link that was banned
            print('{} caused an error and was banned. Now there are {} banned links'.format(url, len(banned['ban'])))