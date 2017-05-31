class DBCRUD(object):
    @staticmethod
    def update_record(new_rec_dic ,query_instance):
        db_rec = {}
        for key in new_rec_dic.keys():
            try:
                #print("check here: ", query_instance.ip)
                db_val = getattr(query_instance,key)
                #print(db_val)
                db_rec[key] = db_val
            except Exception as e:
                print(e)
                return -1
        for key in db_rec.keys():
            if not db_rec[key] or new_rec_dic[key] != db_rec[key]:
                #query_instance.key = new_rec_dic[key]
                setattr(query_instance,key,new_rec_dic[key])
            else:
                pass
        return 0