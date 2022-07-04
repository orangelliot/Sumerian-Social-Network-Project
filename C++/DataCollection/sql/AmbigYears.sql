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
Select * from 
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
inner join
(Select rawnames.tabid as TabID, rawnames.name as Names, amar.year as Year from
rawnames inner join (Select * from bestyears where year like 'amar-sin 6b') as amar
on rawnames.tabid = amar.tabid
where rawnames.name not like '...') as C
on A.Names = C.Names
group by A.Names;

/*Ambiguous tablets that belong to sulgi 42*/
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

/*Ambiguous tablets that belong to amar-suen 6*/
select * from
(Select rawnames.tabid as TabID, rawnames.name as Names, ambig.year as Year from
rawnames inner join (select * from rawyears where year like 'mu sza3-asz-ru-um{ki} ba-hul ') as ambig 
on rawnames.tabid = ambig.tabid
where rawnames.name not like '...') as A
inner join 
(Select rawnames.tabid as TabID, rawnames.name as Names, amar.year as Year from
rawnames inner join (Select * from bestyears where year like 'amar-sin 6b') as amar
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

/* find all years where someone with a name on an ambiguous tablets show up */
select DISTINCT bestyears.year  , rawnames.name from  bestyears 
    JOIN rawnames ON bestyears.tabid = rawnames.tabid 
    where not bestyears.year like "%ur-namma%" and not bestyears.year like "%ibbi-suen%" and not bestyears.year like "%?%" and
    not rawnames.name = "|SZU+LAGAB|" and not rawnames.name = "ur-{d}li9-si4" and not rawnames.name = "ARAD2-zu" and 
    not rawnames.name = "ur-nigar{gar}" and not rawnames.name = "ur-{gesz}gigir" and not rawnames.name = "ur-{d}suen" and not rawnames.name = "la2-ia3" and 
    rawnames.name in
    (select rawnames.name from  rawyears 
	JOIN rawnames ON rawyears.tabid = rawnames.tabid 
    where  rawyears.year like  "mu sza3-asz-ru-um{ki} ba-hul " and not rawnames.name =  "..."
    Group by rawnames.name);