from schema import ServiceConfig, TicketConfig

ysf_2022 = ServiceConfig(
    id= 'ysf-2022',
    name= 'YSF 2022',
    ticket_config=TicketConfig(
        registration_template=r'static/ysf-2022/ticket_template.png',
        registration_color=(255, 255, 255),
        font_family='static/ysf-2022/Poppins/Poppins-Black.ttf',
        offset=(64, 256),
        max_font_size=134,
        max_text_size=1095,
        multi_line=True
    )
)

nexlds_ife = ServiceConfig(
    id= 'nexlds-ife',
    name= 'NEXLDS Ife',
    ticket_config= TicketConfig(
        registration_template = r'static/nexlds-ife/ticket_template.png',
        registration_color = (102, 78, 59),
        font_family = 'static/nexlds-ife/Space_Mono/SpaceMono-Bold.ttf',
        offset = (190, 351),
        max_font_size = 84,
        max_text_size = 693
    )
)

nts_ilorin = ServiceConfig(
    id= 'nts-ilorin',
    name= 'NTS Ilorin',
    ticket_config= TicketConfig(
        registration_template = r'static/nts-ilorin/ticket.png',
        registration_color = (255, 255, 255),
        font_family = 'static/nts-ilorin/Afronik/Afronik.ttf',
        offset = (380, 1000),
        max_font_size = 115,
        max_text_size = 1500,
    )
)

service_configs: dict[str, ServiceConfig] = {
    nexlds_ife.id: nexlds_ife,
    ysf_2022.id: ysf_2022,
    nts_ilorin.id: nts_ilorin,
}
