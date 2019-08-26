import dropbox
from progress.bar import Bar

access_token = ''

dbx = dropbox.Dropbox(access_token)
dbx.users_get_current_account()

# Dropbox Files
class Entry:
    def __init__(self, entry):
        try:
            self.id = entry.id
            self.name = entry.name
            self.path = entry.path_display
            self.size = entry.size
            self.hash = entry.content_hash
        except:
            self.id = None
            self.name = None
            self.path = None
            self.size = None
            self.hash = None

def remove_duplicate_dropbox_photos(path):
    print('______LOOKING FOR DUPLICATES')
    entries = []
    res_entries = []
    dupe_count = 0

    res = dbx.files_list_folder(path, recursive=True)
    res_entries += res.entries
    while res.has_more:
        res = dbx.files_list_folder_continue(res.cursor)
        res_entries += res.entries

    [entries.append(Entry(e)) for e in Bar('Processing Entries').iter(res_entries) if "." in e.path_display]

    for e in Bar('Finding Duplicates').iter(entries):
        dupes = list(filter(lambda x: x.hash == e.hash, entries))

        if len(dupes) > 1:
            for i, d in enumerate(dupes):
                entries.remove(d)
                if i != 0 and d.path is not None:
                    dbx.files_delete_v2(d.path)
                    dupe_count += 1
    return print('____ ' + str(dupe_count) + ' duplicate images removed')

def main():

    folder = ''
    remove_duplicate_dropbox_photos(folder)

if __name__ == '__main__':
    main()
