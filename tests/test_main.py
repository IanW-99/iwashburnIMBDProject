import main


def test_getTop250Tv():
    test_data = main.get_top_250_tv()
    assert len(test_data["items"]) == 250


def test_dbCreation_and_dbFilling():
    testHeadlineDict = {"items": [{'id': 't0000000', 'rank': 1, 'title': 'test', 'fullTitle': 'test_show',
                        'year': '2022', 'crew': 'Ian Washburn, John Santore', 'imDbRating': '100',
                                   'imDbRatingCount': '1'}], "error msg": 'none'}
    test_databaseName = 'test_db.db'
    conn, curs = main.db_connect(test_databaseName)
    main.create_dataBase_tables(curs)
    main.fill_top_250_tv_table(conn, curs, testHeadlineDict)
    curs.execute('''SELECT title FROM top250TvData WHERE id = ?''', ('t0000000',))
    title = curs.fetchone()[0]
    assert title == 'test'


def test_fillTop250TvData():
    test_data = {"items": [{"id": "tt5491994", "rank": "1", "title": "Planet Earth II",
                            "fullTitle": "Planet Earth II (2016)", "year": "2016",
                            "crew": "David Attenborough, Gordon Buchanan", "imDbRating": "9.5",
                            "imDbRatingCount": "110384"}], "error message": "none"}
    conn, curs = main.db_connect('test_db.db')
    main.fill_top_250_tv_table(conn, curs, test_data)


def test_fillTop250MoviesData():
    test_data = {
        "items": [{"id": "tt5491994", "rank": "1", "title": "Planet Earth II", "fullTitle": "Planet Earth II (2016)",
                   "year": "2016", "crew": "David Attenborough, Gordon Buchanan", "imDbRating": "9.5",
                   "imDbRatingCount": "110384"}], "error message": "none"}
    conn, curs = main.db_connect('test_db.db')
    main.create_dataBase_tables(curs)
    main.fill_top_250_movie_table(conn, curs, test_data)


def test_get_movie_IDs():
    test_data = {"items": [{"id": 'test1', "rankUpDown": "+234"}, {"id": 'test2', "rankUpDown": "+2"},
                           {"id": 'test3', "rankUpDown": "+234"}, {"id": 'test4', "rankUpDown": "-234"},
                           {"id": 'test5', "rankUpDown": "-11"}, {"id": 'test6', "rankUpDown": "+56"}],
                 "error msg": "none"}
    # should return ['test1', 'test3', 'test6', 'test4']
    ids = main.get_movie_IDs(test_data)
    assert ids[0] == 'test1' and ids[1] == 'test3' and ids[2] == 'test6' and ids[3] == 'test4'
