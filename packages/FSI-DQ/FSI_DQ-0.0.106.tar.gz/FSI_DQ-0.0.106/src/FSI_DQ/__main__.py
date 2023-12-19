import logging

import pandas as pd
import pyspark.pandas as ps
import io
import pyspark.pandas as ps
from FSI_DQ.business_contextNB import BusinessContext
from FSI_DQ.AnomalyDetectionNB import AnomalyDetection
from FSI_DQ.StandardizationNB import Standardization

from pyspark.sql import SparkSession


class DataQuality:
    def __init__(self,choice,df,dq_path,partition_field,api_key=None,api_base=None,api_version=None,model_name=None,deployment_name=None,standardization_columns=None,inputfile=None, outputfile=None, column_types=None, columns_and_contamination=None,columns_and_null_handling=None, columns_and_dbscan_params=None):
        
        self.choice=choice
        self.df=df
        self.dq_path=dq_path
        # self.catalog_name=catalog_name
        # self.schema=schema
        self.partition_field=partition_field #""
        

        # self.input_table=input_table


        self.api_key=api_key
        self.api_base=api_base
        self.api_version=api_version
        self.deployment_model=deployment_name
        self.model_name=model_name
        

        self.standardization_columns=standardization_columns

        self.column_types=column_types
        self.columns_and_contamination=columns_and_contamination
        self.columns_and_null_handling=columns_and_null_handling
        self.columns_and_dbscan_params=columns_and_dbscan_params
        
        
    
    def write_delta(self,df, path, partition, write_mode='overwrite', parts=1):
        print('path',path)
        print("partition",partition)
        try:
            if partition:
                print("partition")
                df\
                .coalesce(parts)\
                .write\
                .partitionBy(*list(partition))\
                .format('delta')\
                .mode(write_mode)\
                .option('overwriteSchema', 'true')\
                .option('mergeSchema', 'true')\
                .save(path)
            else:
                print('No partition')
                df\
                .coalesce(parts)\
                .write\
                .format('delta')\
                .mode(write_mode)\
                .option('overwriteSchema', 'true')\
                .option('mergeSchema', 'true')\
                .save(path)
        except Exception as e:
            print('writing delta', path, e)




    def main(self):

        try:
            
            spark = SparkSession.builder \
                        .appName("AppName") \
                        .getOrCreate()
            
            # spark.sql(f"USE CATALOG {self.catalog_name}")

            df=self.df.toPandas()
            # df=ps.from_pandas(df)
            print('skipping dq rules')

            if self.choice['DQRules']==5:
                bc_df=df.head(10)
                businessContext= BusinessContext(spark,self.api_key,self.api_base,self.api_version,self.deployment_model,self.model_name)
                result_bc= businessContext.business_contextFN(bc_df)
                #final_table=f"{self.schema}.BusinessContext" #{self.catalog_name}.
                #result_bc.write.option("catalog", self.catalog_name).option("name", final_table).mode('overwrite').saveAsTable(final_table)
                self.write_delta(result_bc, self.dq_path+"/BusinessContext/",self.partition_field)
            
                businessContext= BusinessContext(spark,self.api_key,self.api_base,self.api_version,self.deployment_model,self.model_name)
                result_dq= businessContext.dq_rulesFN(df)
                #final_table=f"{self.schema}.DQRules" #{self.catalog_name}.
                #result_dq.write.option("catalog", self.catalog_name).option("name", final_table).mode('overwrite').saveAsTable(final_table)
                self.write_delta(result_dq, self.dq_path+"/DQRules/",self.partition_field)

            if self.choice['Standardization']==1:
                result=Standardization(spark,self.standardization_columns,df,self.api_key,self.api_base,self.api_version,self.deployment_model,self.model_name).format_issue_detection()
                #final_table=f"{self.schema}.StandardizationResult"#{self.catalog_name}.
                #result.write.option("catalog", self.catalog_name).option("name", final_table).mode('overwrite').saveAsTable(final_table)
                print(result)
                print(result.count())
                self.write_delta(result, self.dq_path+"/standardizationResult/",self.partition_field)
                final_table="StandardizationResult"
                spark.sql('USE CATALOG fsi_uap_framework')
                spark.sql(' USE SCHEMA data_quality_results')
                result.write.option("catalog", 'fsi_uap_framework').option("name", final_table).mode('overwrite').saveAsTable(final_table)
            print('standardization finished')
            print('started anomaly detection')
            
            if self.choice['AnomalyDetection']==1:

                # print(df.head(10))
                df_new=df.head(100000)
                print(len(df_new))
                print( self.column_types, self.columns_and_contamination,
                    self.columns_and_null_handling, self.columns_and_dbscan_params)

                result=AnomalyDetection( self.column_types, self.columns_and_contamination,
                    self.columns_and_null_handling, self.columns_and_dbscan_params).run_anomaly_detection(df_new)
                #final_table=f"{self.schema}.AnomalyDetectionResult"#{self.catalog_name}.
                

                result_sp=spark.createDataFrame(result)
                print('detected anomaly , created df')
                #result_sp.write.option("catalog", self.catalog_name).option("name", final_table).mode('overwrite').saveAsTable(final_table)
                path=self.dq_path+"AnomalyDetectionResult/"

                print('writing as delta')
                self.write_delta(result_sp, path,partition=self.partition_field)
                final_table="data_quality_results.AnomalyResult"
                spark.sql('USE CATALOG fsi_uap_framework')
                spark.sql(' USE SCHEMA data_quality_results')
                result.write.option("catalog", 'fsi_uap_framework').option("name", final_table).mode('overwrite').saveAsTable(final_table)

            

        except Exception as e:
            raise Exception (e)