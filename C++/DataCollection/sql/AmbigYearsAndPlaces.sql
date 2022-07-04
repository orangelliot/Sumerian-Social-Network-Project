/*Query 1: Selects all tablets that contain the ambiguous year*/
select * from rawyears where year like 'mu sza3-asz-ru-um{ki} ba-hul ';

/*Query 2: Select all tablets that contain Sulgi 42*/
Select * from bestyears where year like 'sulgi 42a';

/*Query 3: Select all tablets that contain Amar Suen 6*/
Select * from bestyears where year like 'amar-sin 6b';

/*Query 4: Select all names that appear on tablets belonging to the ambiguous year*/
Select rawnames.tabid as TabID, rawnames.name as Names, ambig.year as Year from
rawnames inner join (select * from rawyears where year like 'mu sza3-asz-ru-um{ki} ba-hul ') as ambig 
on rawnames.tabid = ambig.tabid
where rawnames.name not like '...'
group by Names;

/*Query 5: Select all names that appear on tablets belonging to sulgi 42*/
Select rawnames.tabid as TabID, rawnames.name as Names, sulgi.year as Year from
rawnames inner join (Select * from bestyears where year like 'sulgi 42a') as sulgi
on rawnames.tabid = sulgi.tabid
where rawnames.name not like '...'
group by Names;

/*Query 6: Select all names that appear on tablets belonging to amar-suen 6*/
Select rawnames.tabid as TabID, rawnames.name as Names, amar.year as Year from
rawnames inner join (Select * from bestyears where year like 'amar-sin 6b') as amar
on rawnames.tabid = amar.tabid
where rawnames.name not like '...'
group by Names;

/*Query 7: Select all names that appear in both sulgi 42 and the ambiguous year*/
select * from
(Select rawnames.tabid as TabID, rawnames.name as Names, ambig.year as Year from
rawnames inner join (select * from rawyears where year like 'mu sza3-asz-ru-um{ki} ba-hul ') as ambig 
on rawnames.tabid = ambig.tabid
where rawnames.name not like '...') as A
inner join 
(Select rawnames.tabid as TabID, rawnames.name as Names, sulgi.year as Year from
rawnames inner join (Select * from bestyears where year like 'sulgi 42a') as sulgi
on rawnames.tabid = sulgi.tabid
where rawnames.name not like '...') as B
on A.Names = B.Names
group by A.Names;

/*Query 8: Select all names that appear in both amar-suen 6 and the ambiguous year*/
select * from
(Select rawnames.tabid as TabID, rawnames.name as Names, ambig.year as Year from
rawnames inner join (select * from rawyears where year like 'mu sza3-asz-ru-um{ki} ba-hul ') as ambig 
on rawnames.tabid = ambig.tabid
where rawnames.name not like '...') as A
inner join 
(Select rawnames.tabid as TabID, rawnames.name as Names, amar.year as Year from
rawnames inner join (Select * from bestyears where year like 'amar-sin 6b') as amar
on rawnames.tabid = amar.tabid
where rawnames.name not like '...') as C
on A.Names = C.Names
group by A.Names;

/*Query 9: Select all common names that appear between ambiguous, sulgi 42 and amar-suen 6*/
(Select * from 
(Select rawnames.tabid as TabID , rawnames.name as Names, ambig.year as Year, ambig.translated as Place, ambig.tag as Tag, '' from
rawnames inner join (Select rawyears.tabid, rawyears.year, places.translated, places.tag from rawyears inner join places on places.tabid = rawyears.tabid where year like 'mu sza3-asz-ru-um{ki} ba-hul ') as ambig 
on rawnames.tabid = ambig.tabid
where rawnames.name not like '...') as A
inner join
(Select rawnames.tabid as TabID, rawnames.name as Names, sulgi.year as Year, sulgi.translated as Place, sulgi.Tag as Tag, '' from
rawnames inner join (Select bestyears.tabid, bestyears.year, places.translated, places.tag from bestyears inner join places on places.tabid = bestyears.tabid where year like 'sulgi 42a') as sulgi
on rawnames.tabid = sulgi.tabid
where rawnames.name not like '...') as B
on A.Names = B.Names
inner join
(Select rawnames.tabid as TabID, rawnames.name as Names, amar.year as Year, amar.translated as Place, amar.tag as Tag from
rawnames inner join (Select bestyears.tabid, bestyears.year, places.translated, places.tag from bestyears inner join places on places.tabid = bestyears.tabid where year like 'amar-sin 6b') as amar
on rawnames.tabid = amar.tabid
where rawnames.name not like '...') as C
on A.Names = C.Names
group by A.Names)
union
(Select L.tabid as TabID, 'ur-{d}li9-si4' as name, 'mu sza3-asz-ru-um{ki} ba-hul ' as Year, L.place as Place, L.tag as Tag, '', 
'P120001' as TabID, 'ur-{d}li9-si4' as name, 'sulgi 42a' as Year, '' as Place, '' as Tag, '',
N.tabid as TabID, 'ur-{d}li9-si4' as name, 'amar-sin 6b' as Year, N.place as Place, N.tag as Tag
From
(select * from places where tabid like 'P113642') as L
inner join
(select * from places where tabid like 'P102171') as N);

/*Ambiguous tablets that belong to sulgi 42*/
(Select L.tabid as TabID, 'inim-{d}szara2' as name, 'mu sza3-asz-ru-um{ki} ba-hul ' as Year, L.place as Place, L.tag as Tag, '', 
'P142276' as TabID, 'inim-{d}szara2' as name, 'sulgi 42a' as Year, '' as Place, '' as Tag
From
(select * from places where tabid like 'P126827') as L)
union
(select * from
(Select rawnames.tabid as TabID, rawnames.name as Names, ambig.year as Year, ambig.translated as Place, ambig.tag as Tag, '' from
rawnames inner join (Select rawyears.tabid, rawyears.year, places.translated, places.tag from rawyears inner join places on places.tabid = rawyears.tabid where year like 'mu sza3-asz-ru-um{ki} ba-hul ') as ambig 
on rawnames.tabid = ambig.tabid
where rawnames.name not like '...') as A
inner join 
(Select rawnames.tabid as TabID, rawnames.name as Names, sulgi.year as Year, sulgi.translated as Place, sulgi.Tag as Tag from
rawnames inner join (Select bestyears.tabid, bestyears.year, places.translated, places.tag from bestyears inner join places on places.tabid = bestyears.tabid where year like 'sulgi 42a') as sulgi
on rawnames.tabid = sulgi.tabid
where rawnames.name not like '...') as B
on A.Names = B.Names
where A.Names not in
(Select D.Names from 
(Select rawnames.tabid as TabID, rawnames.name as Names, ambig.year as Year from
rawnames inner join (select * from rawyears where year like 'mu sza3-asz-ru-um{ki} ba-hul ') as ambig 
on rawnames.tabid = ambig.tabid
where rawnames.name not like '...') as D
inner join
(Select rawnames.tabid as TabID, rawnames.name as Names, sulgi.year as Year from
rawnames inner join (Select * from bestyears where year like 'sulgi 42a') as sulgi
on rawnames.tabid = sulgi.tabid
where rawnames.name not like '...') as E
on D.Names = E.Names
inner join
(Select rawnames.tabid as TabID, rawnames.name as Names, amar.year as Year from
rawnames inner join (Select * from bestyears where year like 'amar-sin 6b') as amar
on rawnames.tabid = amar.tabid
where rawnames.name not like '...') as C
on D.Names = C.Names)
group by A.Names);

/*Ambiguous tablets that belong to amar-suen 6*/
select * from
(Select rawnames.tabid as TabID, rawnames.name as Names, ambig.year as Year, ambig.translated as Place, ambig.tag as Tag, '' from
rawnames inner join (Select rawyears.tabid, rawyears.year, places.translated, places.tag from rawyears inner join places on places.tabid = rawyears.tabid where year like 'mu sza3-asz-ru-um{ki} ba-hul ') as ambig 
on rawnames.tabid = ambig.tabid
where rawnames.name not like '...') as A
inner join 
(Select rawnames.tabid as TabID, rawnames.name as Names, amar.year as Year, amar.translated as Place, amar.tag as Tag from
rawnames inner join (Select bestyears.tabid, bestyears.year, places.translated, places.tag from bestyears inner join places on places.tabid = bestyears.tabid where year like 'amar-sin 6b') as amar
on rawnames.tabid = amar.tabid
where rawnames.name not like '...') as B
on A.Names = B.Names
where A.Names not in
(Select D.Names from 
(Select rawnames.tabid as TabID, rawnames.name as Names, ambig.year as Year from
rawnames inner join (select * from rawyears where year like 'mu sza3-asz-ru-um{ki} ba-hul ') as ambig 
on rawnames.tabid = ambig.tabid
where rawnames.name not like '...') as D
inner join
(Select rawnames.tabid as TabID, rawnames.name as Names, sulgi.year as Year from
rawnames inner join (Select * from bestyears where year like 'sulgi 42a') as sulgi
on rawnames.tabid = sulgi.tabid
where rawnames.name not like '...') as E
on D.Names = E.Names
inner join
(Select rawnames.tabid as TabID, rawnames.name as Names, amar.year as Year from
rawnames inner join (Select * from bestyears where year like 'amar-sin 6b') as amar
on rawnames.tabid = amar.tabid
where rawnames.name not like '...') as C
on D.Names = C.Names)
group by A.Names;






