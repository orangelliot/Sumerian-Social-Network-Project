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





