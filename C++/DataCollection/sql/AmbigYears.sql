/*Ambig Years*/
select * from rawyears where year like 'mu sza3-asz-ru-um{ki} ba-hul ';

/*Sulgi 42*/
Select * from bestyears where year like 'sulgi 42a';

/*Amar Suen 6*/
Select * from bestyears where year like 'amar-sin 6b';

/*Ambig Names*/
Select rawnames.tabid as TabID, rawnames.name as Names, ambig.year as Year from
rawnames inner join (select * from rawyears where year like 'mu sza3-asz-ru-um{ki} ba-hul ') as ambig 
on rawnames.tabid = ambig.tabid
where rawnames.name not like '...'
group by Names;

/*Sulgi 42 Names*/
Select rawnames.tabid as TabID, rawnames.name as Names, sulgi.year as Year from
rawnames inner join (Select * from bestyears where year like 'sulgi 42a') as sulgi
on rawnames.tabid = sulgi.tabid
where rawnames.name not like '...'
group by Names;

/*Amar Suen 6 Names*/
Select rawnames.tabid as TabID, rawnames.name as Names, amar.year as Year from
rawnames inner join (Select * from bestyears where year like 'amar-sin 6b') as amar
on rawnames.tabid = amar.tabid
where rawnames.name not like '...'
group by Names;


/*Common names between Ambig, Sulgi and Amar*/
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

/*Select all from Ambig and Sulgi on same Names*/
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

/*Select all from Ambig and Amar on same Names*/
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

/*Select all from Ambig and Amar on same Names*/
select * from
(Select rawnames.tabid as TabID, rawnames.name as Names, sulgi.year as Year from
rawnames inner join (Select * from bestyears where year like 'sulgi 42a') as sulgi
on rawnames.tabid = sulgi.tabid
where rawnames.name not like '...') as B
inner join 
(Select rawnames.tabid as TabID, rawnames.name as Names, amar.year as Year from
rawnames inner join (Select * from bestyears where year like 'amar-sin 6b') as amar
on rawnames.tabid = amar.tabid
where rawnames.name not like '...') as C
on B.Names = C.Names
group by B.Names;

/*Ambig that probs belong to Sulgi*/
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

/*Ambig that probs belong to Amar*/
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