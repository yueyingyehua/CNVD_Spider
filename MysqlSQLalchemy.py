#coding:utf-8

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative

engine =  sqlalchemy.create_engine("mysql+pymysql://root:123456@localhost/cnvd?charset=utf8", encoding = 'utf-8',echo=True)
BaseModel = sqlalchemy.ext.declarative.declarative_base()

class CNVD(BaseModel):
    __tablename__ = "cnvd"
    __table_args__ = {
        "mysql_charset": "utf8"
    }

    id = sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True)
    chname = sqlalchemy.Column("chname",sqlalchemy.String(255), nullable = False, server_default='')
    cnvd_id = sqlalchemy.Column('cnvd_id',sqlalchemy.String(255),nullable= False, server_default='')
    vul_description = sqlalchemy.Column('vul_description',sqlalchemy.Text(),nullable=False)
    vul_solution = sqlalchemy.Column('vul_solution',sqlalchemy.Text(),nullable=False)
    vul_attachment = sqlalchemy.Column('vul_attachment',sqlalchemy.Text(),nullable=False)
    vul_type = sqlalchemy.Column('vul_type',sqlalchemy.String(255),nullable=False, server_default= '')
    vul_level = sqlalchemy.Column('vul_level',sqlalchemy.String(255),nullable=False, server_default= '')
    cve_id = sqlalchemy.Column('cve_id',sqlalchemy.String(255),nullable=False, server_default= '')
    impact_product = sqlalchemy.Column('impact_product',sqlalchemy.Text(),nullable=False)
    validation_info = sqlalchemy.Column('validation_info',sqlalchemy.String(255),nullable=False, server_default= '')
    finder = sqlalchemy.Column('finder',sqlalchemy.String(255),nullable=False, server_default= '')
    reference_link = sqlalchemy.Column('reference_link',sqlalchemy.Text(),nullable=False)
    vendor_patch = sqlalchemy.Column('vendor_patch',sqlalchemy.Text(), nullable=False)
    update_time = sqlalchemy.Column('update_time',sqlalchemy.TIMESTAMP(), nullable=False, server_default = '1970-01-02 00:00:00')
    included_time = sqlalchemy.Column('included_time',sqlalchemy.TIMESTAMP(), nullable=False, server_default = '1970-01-02 00:00:00')
    submission_time = sqlalchemy.Column('submission_time',sqlalchemy.TIMESTAMP(), nullable=False, server_default = '1970-01-02 00:00:00')
    release_time = sqlalchemy.Column('release_time',sqlalchemy.TIMESTAMP(), nullable=False, server_default = '1970-01-02 00:00:00')
    bugtraq_id = sqlalchemy.Column('bugtraq_id',sqlalchemy.String(255), nullable=False, server_default= '')


class CNNVD(BaseModel):
    __tablename__ = "cnnvd"
    __table_args__ = {
        "mysql_charset": "utf8"
    }

    id = sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, autoincrement=True)
    chname = sqlalchemy.Column("chname", sqlalchemy.String(255), nullable=False, server_default='')
    cnnvd_id = sqlalchemy.Column("cnnvd_id", sqlalchemy.String(255), nullable=False, server_default= '')
    release_time = sqlalchemy.Column("release_time", sqlalchemy.TIMESTAMP, nullable=False, server_default= '1970-01-02 00:00:00')
    update_time = sqlalchemy.Column("update_time", sqlalchemy.TIMESTAMP, nullable=False, server_default= '1970-01-02 00:00:00')
    vul_level = sqlalchemy.Column("vul_level", sqlalchemy.String(255), nullable=False, server_default= '')
    vul_type = sqlalchemy.Column("vul_type", sqlalchemy.String(255), nullable=False, server_default='')
    Threat_type = sqlalchemy.Column("Threat_type", sqlalchemy.String(255), nullable=False, server_default='')
    cve_id = sqlalchemy.Column("cve_id", sqlalchemy.String(255), nullable=False, server_default='')
    source_of_vul = sqlalchemy.Column('source_of_vul', sqlalchemy.String(255), nullable=False, server_default='')
    vul_description = sqlalchemy.Column('vul_description', sqlalchemy.Text(), nullable=False)
    vul_announcement = sqlalchemy.Column("vul_announcement", sqlalchemy.Text(), nullable=False)
    reference_link = sqlalchemy.Column("reference_link", sqlalchemy.Text(), nullable=False)




class MysqlSQLalchemy():

    def __init__(self):
        self.DBSessinon = sqlalchemy.orm.sessionmaker(bind = engine)
        self.session = self.DBSessinon()
        BaseModel.metadata.create_all(engine)

    def CNVD_insert(self,messageResult):
        try:
            cnvd = CNVD(chname = messageResult['chname'],
                        cnvd_id = messageResult['cnvd_id'],
                        cve_id = messageResult['cve_id'],
                        finder = messageResult['finder'],
                        impact_product = messageResult['impact_product'],
                        included_time = messageResult['included_time'],
                        release_time = messageResult['release_time'],
                        reference_link = messageResult['reference_link'],
                        submission_time = messageResult['submission_time'],
                        update_time = messageResult['update_time'],
                        validation_info = messageResult['validation_info'],
                        vendor_patch = messageResult['vendor_patch'],
                        vul_attachment = messageResult['vul_attachment'],
                        vul_description = messageResult['vul_description'],
                        vul_level = messageResult['vul_level'],
                        vul_solution = messageResult['vul_solution'],
                        vul_type = messageResult['vul_type'],
                        bugtraq_id = messageResult['bugtraq_id']
                        )
            self.session.add(cnvd)
            self.session.commit()
        except Exception as excep:
            self.session.rollback()
            raise
        self.session.close()

    def CNVD_selectBycnvdId(self, cnvdId):
        return self.session.query(CNVD).filter_by(cnvd_id=cnvdId).all()

    def CNNVD_insert(self,messageResult):
        try:
            cnnvd = CNNVD(chname = messageResult['chname'],
                          cnnvd_id = messageResult['cnnvd_id'],
                          cve_id = messageResult['cve_id'],
                          release_time = messageResult['release_time'],
                          update_time = messageResult['update_time'],
                          vul_level = messageResult['vul_level'],
                          vul_type = messageResult['vul_type'],
                          Threat_type = messageResult['Threat_type'],
                          source_of_vul = messageResult['source_of_vul'],
                          vul_description = messageResult['vul_description'],
                          vul_announcement = messageResult['vul_announcement'],
                          reference_link = messageResult['reference_link']
                        )
            self.session.add(cnnvd)
            self.session.commit()
        except Exception as excep:
            self.session.rollback()
            raise
        self.session.close()