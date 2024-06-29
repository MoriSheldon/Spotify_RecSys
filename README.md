This toy project about building RecSys from ground up myself
Since there's only me as a user, input
I can not try collaborative filtering
I would be using content based filtering(user-song interaction)
Plus, I will later on add clustering method to make system hybrid

I'm using pytorch template
https://github.com/victoresque/pytorch-template
Made this project so much easier to start

As for the dataset I'm using, I got 1 million songs from spotify
https://www.kaggle.com/datasets/amitanshjoshi/spotify-1million-tracks?select=spotify_data.csv
Which also has genre column not obtainable from Spotify API
Using genre to filter out songs that are far from my taste before sampling
But I might have to get features from sample songs again cuz they lack some features