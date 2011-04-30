#!/usr/bin/python
import gdata.docs.service
import gdata.youtube
import gdata.youtube.service
import sys

# Create a client class which will make HTTP requests with Google Docs server.
Hclient = gdata.docs.service.DocsService()
# Authenticate using your Google Docs email address and password.
#client.ClientLogin('cgnetswarachannel@gmail.com', 'kissmyass3ce')

# Query the server for an Atom feed containing a list of your documents.
#documents_feed = client.GetDocumentListFeed()
# Loop through the feed and extract each document entry.
#for document_entry in documents_feed.entry:
  # Display the title of the document on the command line.
 # print document_entry.title.text

yt_service = gdata.youtube.service.YouTubeService()

# The YouTube API does not currently support HTTPS/SSL access.
yt_service.ssl = False
yt_service.developer_key = "AI39si5pjJmhiUXuwBzzIaXhx39O3USda1v40n7QPkHyw51jBsQLVs9qSD1Ilh9U2-Ny3466flm4lDDA2lpGxhqU1FCy1a7fsw"


yt_service.email = 'cgnetswarachannel@gmail.com'
yt_service.password = 'kissmyass3ce'
yt_service.ProgrammaticLogin()


# prepare a media group object to hold our video's meta-data
my_media_group = gdata.media.Group(
  title=gdata.media.Title(text='My Test Movie'),
  description=gdata.media.Description(description_type='plain',
                                      text='My description'),
  keywords=gdata.media.Keywords(text='cars, funny'),
  category=[gdata.media.Category(
      text='Autos',
      scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
      label='Autos')],
  player=None
)


# prepare a geo.where object to hold the geographical location
# of where the video was recorded
where = gdata.geo.Where()
where.set_location((37.0,-122.0))

# create the gdata.youtube.YouTubeVideoEntry to be uploaded
video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group,
                                              geo=where)

# set the path for the video file binary
video_file_location = sys.argv[1]

new_entry = yt_service.InsertVideoEntry(video_entry, video_file_location)

print new_entry.media.player.url.split('&')[0]

