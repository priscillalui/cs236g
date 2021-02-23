import pandas as pd
from langdetect import detect

df_1 = pd.read_csv('images.csv')
df_3 = pd.read_csv('images3.csv')
df = df_1.append(df_3)
print(df.shape)
df.to_csv('images_all.csv')

### Filters based on images
print('Filtering based on size....')
dimension_condition_x = df['xdim'] > 100
dimension_condition_y = df['ydim'] > 100
df2 = df[dimension_condition_x & dimension_condition_y]
print(df2.shape)

#### Filters based on texts
print('Filtering based on detected language...')
def _is_english(value):
    try:
        if detect(value)=='en':
            return True
        else:
            return False
    except:
        return False

df3 = df2[df2.text.apply(lambda x : isinstance(x,str))]
df4 = df3[df3.text.apply(lambda x : _is_english(x))]
print(df4.shape)

df2.to_csv('images_filtered_by_dims.csv')
df4.to_csv('images_filtered_by_dims_and_lang.csv')
#df3 = df2[df2.text.apply(lambda x : isinstance(x,str))]
#df4 = df3[df3.text.apply(lambda x : _is_english(x))]

