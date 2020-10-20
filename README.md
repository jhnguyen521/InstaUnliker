# InstaUnliker
Unlike recently liked Instagram posts.
Quickly scrapped together in response to https://www.reddit.com/r/Adblock/comments/jc447f/nano_adblocker_nano_defender_was_sold_and_should/

## Instructions
1. ``pip install -r requirements.txt``
2. ``python unliker.py USERNAME PASSWORD MAX_TO_REMOVE(OPTIONAL)``
3. If you want to add optional filtering, you can create a filter function in the code and add it to the list passed into unliker.unlike()

## Important
Make sure to not unlike a large amount of photos in a short period of time. Not sure how the automation detection works but Instagram will lock/limit your account in the event that you are somehow flagged. I suggest rerunning the script once every day or so.
