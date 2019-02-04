
begin transaction;

create table targets (id integer primary key autoincrement not null, target text not null, unique(target));
insert into targets (target) select distinct target from results;

create table results2 (type text not null, target_id integer not null, time real not null, result real not null);
insert into results2 select type, targets.id, time, result from results inner join targets where targets.target = results.target;

drop table results;
alter table results2 rename to results;

create index target_time on results (target_id, time);

commit transaction;

vacuum;

explain query plan select targets.target, time, result from results inner join targets where time > 1549172399 and time < 1549272399 and targets.id = results.target_id order by time;
select count(*) from (select targets.target, time, result from results inner join targets where targets.id = results.target_id);
