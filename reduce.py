import pandas as pd

df = pd.read_pickle('tmp.pkl')

params_remove = [
    'limitno',
    'q',
    'v',
    'c',
    'm',
    'a',
    'v',
    'w',
    'postcode',
    'responsive',
    'searchsuburb',
    'jinvid',
    'jassignid',
    'checksum',
    'style',
    'src_type',
    'answer',
    'sub_type',
    'enable_hui_body',
    'source',
    'device_token',
    'cr',
    'lz',
    'sms_source',
    'redirect',
    'dcr',
    'url',
    'from'

]

def remove_params(url):
    retain = []
    if "?" in url:
        t1  = url.partition('?')
        if len(t1) ==3:
            path = t1[0]
            params = t1[2]
        else:
            return url

        npl = params.split('&')
        for np in npl:
            if "=" in np:
                t2 = np.partition('=')
                if len(t2)==3:
                    k = t2[0]
                    v = t2[2]
                else:
                    continue

                if v == None:
                    continue
                if k in params_remove:
                    continue
                else:
                    retain.append(np)
        if len(retain)>0:
            return path + "?" + "&".join(retain)
        else:
            return path
    else:
        return url


df['tmp'] = df['pagePath'].apply(lambda x: remove_params(x))
reduced_df = df[['tmp','pageviews']].groupby('tmp').sum().sort_values(by='pageviews',ascending=False)
reduced_df.reset_index(inplace=True)
reduced_df.rename(columns={'tmp':'New Page Path'}, inplace=True)
max_rows = df.shape[0]
retained_rows = reduced_df.shape[0]
reduction = max_rows - retained_rows
reduction_rate = reduction/max_rows
print("{} was {} saved {:.2f}%".format(retained_rows,max_rows, reduction_rate*100))

print(reduced_df.head(20))