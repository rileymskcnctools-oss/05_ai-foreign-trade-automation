"""注入测试数据到 data/ft_workspace.db (正确的数据库)"""
import sqlite3

conn = sqlite3.connect("data/ft_workspace.db", timeout=10)

# ===== 1. 客户 =====
clients = [
    ("AfroFarm Ltd","Nigeria","www.afrofarm.ng","Chukwuemeka Obi","chukwuemeka@afrofarm.ng","+234****5678","+234****5678","","importer","Hand tools, farm implements","West Africa","50000","A",85,"alibaba","Large importer of Chinese hand tools","customer"),
    ("GreenFields GmbH","Germany","www.greenfields.de","Hans Mueller","hans@greenfields.de","+493****3456","+493****3456","linkedin.com/in/hansmueller","distributor","Garden tools, professional farming","Europe","30000","A",78,"trade_show","Premium European distributor","customer"),
    ("Savanna Supplies","Kenya","www.savanna.co.ke","James Mwangi","james@savanna.co.ke","+254****5678","+254****5678","","retailer","Farm tools, agricultural supplies","East Africa","20000","B",65,"referral","Growing retailer in Kenya","contacted"),
    ("Outback Agri","Australia","www.outbackagri.com.au","Tom Wilson","tom@outbackagri.com.au","+614****5678","+614****5678","linkedin.com/in/tomwilson","distributor","Professional farming tools","Oceania","15000","A",72,"cold_call","Interested in premium hoe range","interested"),
    ("Ferme du Sahel","Burkina Faso","","Ibrahim Compaore","ibrahim@fermesahel.bf","+226****3456","+226****3456","","importer","Basic farm tools","West Africa","10000","C",45,"website","Small scale buyer","quoted"),
    ("Baltic Tools OU","Estonia","www.baltictools.ee","Marti Tamm","marti@baltictools.ee","+372****4567","+372****4567","linkedin.com/in/martitamm","distributor","Hand tools, construction","Baltic/Nordic","25000","B",60,"linkedin","Expanding into farm tools","contacted"),
    ("Zambezi Farm","Zambia","","Grace Phiri","grace@zambezifarm.zm","+260****4567","+260****4567","","retailer","Farm implements, seeds","Southern Africa","8000","D",30,"referral","","lead"),
    ("AgriSolutions SA","South Africa","www.agrisolutions.co.za","Pieter van der Berg","pieter@agrisolutions.co.za","+278****4567","+278****4567","linkedin.com/in/pvdberg","distributor","Professional agricultural tools","Southern Africa","40000","A",82,"trade_show","Premium distributor, good volume","negotiating"),
]
for c in clients:
    conn.execute("""INSERT INTO clients
        (company_name,country,website,contact_person,email,phone,whatsapp,linkedin,
         business_type,main_products,market_regions,estimated_volume,grade,grade_score,source,notes,status)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", c)
print(f"Inserted {len(clients)} clients")

# ===== 2. 市场报告 =====
reports = [
    ("Nigeria","Weeding Tools","Nigeria Weeding Tools Market Report 2026",
     "Nigeria is Africa's largest farm tool market with 200M+ population. Weeding hoes dominate demand.",
     "Full report covering market size, competitive landscape, import regulations, pricing trends...",
     None,"Trade Ministry data, Alibaba trends",0.75),
    ("Germany","Cutting Tools","German Garden Tool Market Analysis",
     "Germany leads European garden tool demand. Strong preference for professional-grade tools.",
     "Full analysis of German market including distribution channels, pricing, competition...",
     None,"Eurostat, Trade shows",0.82),
    ("Kenya","Digging Tools","East Africa Agricultural Tools Demand",
     "Kenya is a gateway to East African market. Growing mechanization drives tool demand.",
     "Comprehensive analysis of East African farm tool market...",
     None,"Kenya Bureau of Statistics",0.70),
]
for r in reports:
    conn.execute("""INSERT INTO market_reports
        (country,product_category,report_title,summary,full_report,report_file,data_sources,confidence)
        VALUES (?,?,?,?,?,?,?,?)""", r)
print(f"Inserted {len(reports)} market reports")

# ===== 3. 市场知识 =====
knowledge = [
    ("Nigeria","Weeding Tools","Nigeria import duty on hand tools is 5-10%. No phytosanitary cert needed for metal tools.","Trade Ministry",1),
    ("Germany","General","CE marking mandatory for garden tools in EU market.","EU Regulation",1),
    ("Kenya","Digging Tools","KEBS certification required for imported hand tools. Process takes 4-6 weeks.","Import Agent",0),
    ("Australia","Cutting Tools","AS/NZS certification required for cutting tools.","Trade Commission",1),
]
for k in knowledge:
    conn.execute("INSERT INTO market_knowledge (country,category,knowledge,source,verified) VALUES (?,?,?,?,?)", k)
print(f"Inserted {len(knowledge)} knowledge entries")

# ===== 4. 活动记录 =====
activities = [
    (1,"email","outbound","Welcome email with catalog","Sent full catalog","completed",None,None,"2026-07-01"),
    (1,"whatsapp","inbound","Re: Catalog inquiry","Interested in round head hoe","completed",None,None,None),
    (1,"email","outbound","Quotation RHH-120","Sent quote for RHH-120","completed",None,"2026-07-10",None),
    (2,"email","outbound","Introduction premium range","Hans responded positively","completed",None,None,None),
    (2,"phone","outbound","Price negotiation call","Discussed FOB pricing","completed",None,"2026-07-08",None),
    (3,"email","outbound","Cold outreach Kenya","Sent initial email","completed",None,None,None),
    (5,"email","inbound","RFQ from Ferme du Sahel","Looking for 3000pcs hoe","completed",None,None,None),
    (5,"email","outbound","Quotation reply","Sent CIF pricing","completed",None,"2026-07-12",None),
    (8,"email","outbound","Premium catalog","Pieter interested","completed",None,None,None),
    (8,"meeting","inbound","Trade show follow-up","Met at Hannover Messe","completed",None,"2026-07-05",None),
    (4,"linkedin","outbound","Connection request","Tom connected","completed",None,None,None),
    (6,"email","outbound","Baltic market intro","Sent catalog to Marti","completed",None,None,None),
    (2,"email","outbound","Follow-up order confirmation","Hans confirmed 3000pcs","completed",None,"2026-07-15",None),
    (8,"whatsapp","outbound","Delivery timeline update","Updated production status","completed",None,"2026-07-20",None),
    (3,"email","outbound","Follow up catalog request","Pending response","pending",None,None,"2026-07-28"),
    (6,"email","outbound","Follow up Baltic tools","Marti not responded","pending",None,None,"2026-07-30"),
]
for a in activities:
    conn.execute("""INSERT INTO activities
        (client_id,activity_type,direction,subject,content,status,scheduled_date,actual_date,follow_up_date)
        VALUES (?,?,?,?,?,?,?,?,?)""", a)
print(f"Inserted {len(activities)} activities")

# ===== 5. 报价 =====
quotations = [
    ("QT-2026-001",1,"RHH-120",2000,3.50,"USD","FOB","Tianjin","T/T 30/70",30,30,7000,"","",
     "accepted"),
    ("QT-2026-002",2,"FGH-080",5000,4.20,"USD","FOB","Tianjin","L/C at sight",45,30,21000,"","",
     "accepted"),
    ("QT-2026-003",5,"FDH-100",3000,3.80,"USD","CIF","Ouagadougou","T/T advance",35,15,11400,"","",
     "sent"),
    ("QT-2026-004",8,"GGT-060",1500,8.50,"USD","FOB","Tianjin","L/C at sight",30,30,12750,"","",
     "negotiating"),
    ("QT-2026-005",1,"WCH-050",3000,2.80,"USD","FOB","Tianjin","T/T 30/70",25,30,8400,"","",
     "sent"),
]
for q in quotations:
    conn.execute("""INSERT INTO quotations
        (quotation_no,client_id,product_code,quantity,unit_price,currency,incoterm,port,
         payment_terms,lead_time_days,validity_days,total_amount,email_body,quotation_file,status)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", q)
print(f"Inserted {len(quotations)} quotations")

# ===== 6. 价格记录 =====
prices = [
    ("RHH-120",2.50,2.00,"West Africa","2026-06-01","Standard round head hoe"),
    ("FGH-080",3.00,2.40,"Europe","2026-06-01","Flat garden hoe"),
    ("FDH-100",2.80,2.20,"West Africa","2026-06-01","Flat digging hoe"),
    ("GGT-060",6.00,4.80,"Oceania","2026-06-01","Premium garden tool"),
    ("WCH-050",2.00,1.60,"Global","2026-06-01","Weeding hoe basic"),
]
for p in prices:
    conn.execute("""INSERT INTO price_records
        (product_code,base_price_usd,min_price_usd,target_market,effective_date,notes)
        VALUES (?,?,?,?,?,?)""", p)
print(f"Inserted {len(prices)} price records")

conn.commit()
conn.close()
print("\n✅ All test data injected into data/ft_workspace.db!")
