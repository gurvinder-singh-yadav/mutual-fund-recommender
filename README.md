# Mutual Fund Recommender
A mutual fund recommendation system using basket of stock of multiple mutual fund managers

## To run api
`uvicorn api:app --reload`

## To update Grow data daily
`python main.py`


## See the following api mapping to get final data
 - "/top_10_volume_grow" -> stops with aggregate volume as maximum
 - "/top_10_popular_grow" -> stocks which are being baught by most of the mutual funds