drop view last_positions;
create view last_positions as SELECT positions.geom,
                                     positions.id,
                                     positions.sensor_id,
                                     positions.current_floor,
                                     positions.current_temperature,
                                     positions.current_speed
                              FROM positions
                              ORDER BY positions.fid DESC
                              LIMIT 4;
INSERT INTO `gpkg_contents`(`table_name`,`data_type`,`identifier`,`min_x`,`min_y`,`max_x`,`max_y`,`srs_id`)
VALUES ('last_positions','features','last_positions',-479163,-1101110,-479106,-1101012,5514);
INSERT INTO `gpkg_geometry_columns`(`table_name`,`column_name`,`geometry_type_name`,`srs_id`,`z`,`m`)
VALUES ('last_positions','geom','Point',5514,0,0);
