import main


def test_getTop250Tv():
    test_data = main.getTop250Tv()
    assert len(test_data["items"]) == 250


def test_dbCreation_and_dbFilling():
    testHeadlineDict = {'t0000000': {'rank': 1, 'title': 'test', 'fullTitle': 'test_show', 'year': '2022',
                                     'crew': 'Ian Washburn, John Santore', 'imdbRating': '100', 'imdbRatingCount': '1'}}
    test_databaseName = 'test_db.db'
    conn, curs = main.dbConnect(test_databaseName)
    main.createDataBase(curs)
    main.fillTop250TvData(conn, curs, testHeadlineDict)
    curs.execute('''SELECT title FROM top250TvData WHERE id = ?''', ('t0000000',))
    title = curs.fetchone()[0]
    assert title == 'test'


def test_fillTop250TvData():
    test_data = {"items": [{"id": "tt5491994", "rank": "1", "title": "Planet Earth II",
                            "fullTitle": "Planet Earth II (2016)", "year": "2016",
                            "crew": "David Attenborough, Gordon Buchanan", "imDbRating": "9.5",
                            "imDbRatingCount": "110384"}], "error message": "none"}
    conn, curs = main.dbConnect('test_db.db')
    main.fillTop250TvData(conn, curs, test_data)


def test_fillTop250MoviesData():
    test_data = {
        "items": [{"id": "tt5491994", "rank": "1", "title": "Planet Earth II", "fullTitle": "Planet Earth II (2016)",
                   "year": "2016", "crew": "David Attenborough, Gordon Buchanan", "imDbRating": "9.5",
                   "imDbRatingCount": "110384"}], "error message": "none"}
    conn, curs = main.dbConnect('test_db.db')
    main.createDataBase(curs)
    main.fillTop250MovieData(conn, curs, test_data)
