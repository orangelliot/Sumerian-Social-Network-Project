name = 'bob'
#print(f'create (n:Name {{name:\'{name}\'}})')

tablet = list(['P1', 'Shulgi1', 100])
#print(f'create (n:Tablet {{tabid:\'{tablet[0]}\', year:\'{tablet[1]}\', sim:{tablet[2]}}})')


#print(f'match (t:Tablet),(n:Name)\nwhere t.tabid=\'{tablet[0]}\' and n.name=\'{name}\'\ncreate (t)-[r:HasName]->(n)')


print(tablet[:-1])