# # import time
# # CREATE_DATE = time.strftime("%d/%m/%Y")
# # CREATE_TIME= time.strftime("%X")
# # print(len(CREATE_DATE))
# # print(len(CREATE_TIME))
# #
# # CURRENT_DATE_TIME = time.strftime("%c")
# # print(CURRENT_DATE_TIME)
#
# <label class="page1">Country</label>
# <div class="tooltips" title="Please select the country that the customer will primarily be served from">
#     <select id="country" name="country" placeholder="Phantasyland">
#         <option></option>
#         <option>Asia</option>
#         <option>Africa</option>
#         <option>Australia</option>
#         <option>Europe</option>
#         <option>North America</option>
#         <option>South America</option>
#     </select>
# </div>
# <br />
# <br />
# <label class="page1">Location</label>
# <div class="tooltips" title="Please select the city that the customer is primarily to be served from.">
#     <select id="location" name="location" placeholder="Anycity"></select>
# </div>
#
# jQuery(function($) {
#     var
# locations = {
# 'Asia':
# ['Afghanistan',
# ' Armenia',
# ' Azerbaijan',
# ' Bahrain',
# ' Bangladesh',
# ' Bhutan',
# ' Brunei',
# ' Myanmar',
# ' Cambodia',
# ' China (PRC)',
# ' India',
# ' Indonesia',
# ' Iran',
# ' Iraq',
# ' Israel',
# ' Japan',
# ' Jordan',
# ' Kazakhstan',
# ' North Korea',
# ' South Korea',
# ' Kuwait',
# ' Kyrgyzstan',
# ' Laos',
# ' Lebanon',
# ' Malaysia',
# ' Maldives',
# ' Mongolia',
# 'Nepal',
# ' Oman',
# ' Pakistan',
# ' Philippines',
# ' Qatar',
# ' Saudi Arabia',
# ' Singapore',
# ' Sri Lanka',
# ' Syria',
# ' Taiwan',
# ' Tajikistan',
# ' Thailand',
# ' Timor-Leste',
# ' Turkmenistan',
# ' United Arab Emirates',
# ' Uzbekistan',
# ' Vietnam',
# ' Yemen'],
#
# 'Africa':
# ['Luanda',
# 'Gaborone',
# 'Bujumbura',
# 'Praia',
# 'N Djamena',
# 'Kinshasa',
# 'Yamoussoukro (seat of government at Abidjan)',
# 'Cairo',
# 'Asmara',
#  'Libreville',
# 'Accra',
# 'Bissau',
# 'Maseru',
# 'Tripoli',
# 'Lilongwe',
# 'Nouakchott',
# 'Mamoudzou',
# 'Maputo',
# 'Niamey',
# 'Saint-Denis',
# 'Jamestown',
# 'Dakar',
# 'Freetown',
# 'Pretoria (administrative), Cape Town (legislative), Bloemfontein (judicial)',
# 'Mbabane (administrative), Lobamba (royal and legislative)',
# 'Lomé',
# 'Kampala',
# 'Lusaka'],
# 'Australia':
# ['Fiji',
# 'Kiribati',
# 'Marshall Islands',
# 'Micronesia',
# 'Nauru',
# 'New Zealand',
# 'Palau',
# 'Papua New Guinea',
# 'Samoa',
# 'Solomon Islands',
# 'Tonga',
# 'Tuvalu',
# 'Vanuatu'
# ],
# 'Europe':
# ['Andorra la Vella',
# 'Minsk',
# 'Sarajevo',
# 'Zagreb',
# 'Copenhagen',
# 'Tórshavn',
# 'Paris',
# 'Gibraltar',
# 'Saint Peter Port',
# 'Reykjavík',
# 'Douglas',
# 'Saint Helier',
# 'Riga',
# 'Vilnius',
# 'Skopje',
# 'Chisinau',
# 'Podgorica',
# 'Oslo',
# 'Lisbon',
# 'Moscow',
# 'Belgrade',
# 'Ljubljana',
# 'Stockholm',
# 'Kiev',
# 'Vatican City',
# ],
# 'North America': ['Puebla'],
# 'South America': ['Midrand'],
# }
#
# var $locations = $('#location');
# $('#country').change(function()
# {
#     var
# country = $(this).val(), lcns = locations[country] | | [];
#
# var
# html = $.map(lcns, function(lcn)
# {
# return '<option value="' + lcn + '">' + lcn + '</option>'
# }).join('');
# $locations.html(html)
# });
# });
