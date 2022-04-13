#     path = 'static/uploads/'
#     uploads = sorted(os.listdir(path), key=lambda x: os.path.getctime(path+x))
#     # print(uploads)
#     #     #uploads = os.listdir('static/uploads')
#     # uploads = ['uploads/' + file for file in uploads]
#     # uploads.reverse()
#     uploads = ['uploads/' + file for file in uploads]
#     uploads.reverse()
#     dictupload=dict()
#     for i in uploads:
#         j=i.split('/')[1]
#         cap=Posts.query.with_entities(Posts.caption).filter_by(pic=j).first()[0]
#         dictupload[i]=cap
#     return render_template("feed.html",dict=dictupload)   