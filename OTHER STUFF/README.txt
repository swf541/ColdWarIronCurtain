## Dynamic HoI4 News Event Headers
----
By Yard1, originally for Equestria at War, concept by Agatha (TWR dev team). Developed independently and does not use any code from TWR or DH.

If you use this kit, please credit Yard1/Equestria at War and Agatha (TWR dev team).

## Usage
----
1. Put all files from this folder into the root of your mod folder. Note: interface/eventwindow.gui and gfx/interface/event_news_bg.dds will be overwritten.

2. Make your own newspaper headers. Go to gfx/interface/newspaper_headers. There is a template there. Make sure to only edit the blue part - the black part is padding to make sure the texticon fits in properly.

3. Add the entries for your newspaper headers to interface/eaw_newspaper_texticons.gfx

4. Add the texticon entries to localisation/eaw_newspaper_headers_l_english.yml - Make sure to keep the exact number of \n. The name after £ is the name of the GFX entry from interface/eaw_newspaper_texticons.gfx

5. Add scripted localisation entries to common\scripted_localisation\EAW_newspaper_headers.txt You can use any triggers you want. The localisation keys are the same you've made in step 4.

6. Run the hoi4newspaperheaderadded.py Python script. Make sure you have Python 3.7. Pass the path to the folder of your mod as an argument, eg. python hoi4newspaperheaderadded.py "Paradox Interactive/mods/my_mod"

Done.

Notes:
You can run the script as many times you want, it will not add the scripted loc call to keys which already have it.

The only change in eventwindow.gui is the following textbox in the news event entry ("EventWindow_News"):

From:

			instantTextBoxType = {
				name = "Title"
				position = { x = 30 y = 260 }
				font = "hoi4_typewriter22"
				borderSize = {x = 0 y = 0}
				text = "Title text here!"	
				maxWidth = 460
				maxHeight = 32
				format = centre
			}
            
To:

			instantTextBoxType = {
				name = "Title"
				position = { x = 30 y = 18 }
				font = "hoi4_typewriter22"
				borderSize = {x = 0 y = 0}
				text = "Title text here!"	
				maxWidth = 460
				maxHeight = 800
				format = centre
			}