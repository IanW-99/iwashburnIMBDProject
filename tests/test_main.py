import main


def test_getTop250Tv():
    test_data = main.getTop250Tv()
    assert len(test_data["items"]) == 250


def test_dbCreation_and_dbFilling():
    testHeadlineDict = {'t0000000': {'title': 'test', 'fullTitle': 'test_show', 'year': '2022',
                        'crew': 'Ian Washburn, John Santore', 'imdbRating': '100', 'imdbRatingCount': '1'}}
    test_databaseName = 'test_db.db'
    conn, curs = main.dbConnect(test_databaseName)
    main.createDataBase(curs)
    main.fillHeadlineData(conn, curs, testHeadlineDict)
    curs.execute('''SELECT title FROM headlineData WHERE id = ?''', ('t0000000',))
    title = curs.fetchone()[0]
    assert title == 'test'
