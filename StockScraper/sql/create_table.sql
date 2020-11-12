create table stock.portfolio (
	portfolio_pky serial primary key,
	participant_id varchar(256),
	name_of_ccass_participant varchar(256),
	address varchar(1024),
	shareholding decimal(20,8),
	percentage decimal(16,8),
	stock_code varchar(10),
	report_date timestamp
	
)