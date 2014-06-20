<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="6.4">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="no" active="no"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="15" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="frames">
<description>&lt;b&gt;Frames for Sheet and Layout&lt;/b&gt;</description>
<packages>
</packages>
<symbols>
<symbol name="LETTER_L">
<frame x1="0" y1="0" x2="248.92" y2="185.42" columns="12" rows="17" layer="94" border-left="no" border-top="no" border-right="no" border-bottom="no"/>
</symbol>
<symbol name="DOCFIELD">
<wire x1="0" y1="0" x2="71.12" y2="0" width="0.1016" layer="94"/>
<wire x1="101.6" y1="15.24" x2="87.63" y2="15.24" width="0.1016" layer="94"/>
<wire x1="0" y1="0" x2="0" y2="5.08" width="0.1016" layer="94"/>
<wire x1="0" y1="5.08" x2="71.12" y2="5.08" width="0.1016" layer="94"/>
<wire x1="0" y1="5.08" x2="0" y2="15.24" width="0.1016" layer="94"/>
<wire x1="101.6" y1="15.24" x2="101.6" y2="5.08" width="0.1016" layer="94"/>
<wire x1="71.12" y1="5.08" x2="71.12" y2="0" width="0.1016" layer="94"/>
<wire x1="71.12" y1="5.08" x2="87.63" y2="5.08" width="0.1016" layer="94"/>
<wire x1="71.12" y1="0" x2="101.6" y2="0" width="0.1016" layer="94"/>
<wire x1="87.63" y1="15.24" x2="87.63" y2="5.08" width="0.1016" layer="94"/>
<wire x1="87.63" y1="15.24" x2="0" y2="15.24" width="0.1016" layer="94"/>
<wire x1="87.63" y1="5.08" x2="101.6" y2="5.08" width="0.1016" layer="94"/>
<wire x1="101.6" y1="5.08" x2="101.6" y2="0" width="0.1016" layer="94"/>
<wire x1="0" y1="15.24" x2="0" y2="22.86" width="0.1016" layer="94"/>
<wire x1="101.6" y1="35.56" x2="0" y2="35.56" width="0.1016" layer="94"/>
<wire x1="101.6" y1="35.56" x2="101.6" y2="22.86" width="0.1016" layer="94"/>
<wire x1="0" y1="22.86" x2="101.6" y2="22.86" width="0.1016" layer="94"/>
<wire x1="0" y1="22.86" x2="0" y2="35.56" width="0.1016" layer="94"/>
<wire x1="101.6" y1="22.86" x2="101.6" y2="15.24" width="0.1016" layer="94"/>
<text x="1.27" y="1.27" size="2.54" layer="94" font="vector">Date:</text>
<text x="12.7" y="1.27" size="2.54" layer="94" font="vector">&gt;LAST_DATE_TIME</text>
<text x="72.39" y="1.27" size="2.54" layer="94" font="vector">Sheet:</text>
<text x="86.36" y="1.27" size="2.54" layer="94" font="vector">&gt;SHEET</text>
<text x="88.9" y="11.43" size="2.54" layer="94" font="vector">REV:</text>
<text x="1.27" y="19.05" size="2.54" layer="94" font="vector">TITLE:</text>
<text x="1.27" y="11.43" size="2.54" layer="94" font="vector">Document Number:</text>
<text x="17.78" y="19.05" size="2.54" layer="94" font="vector">&gt;DRAWING_NAME</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="LETTER_L" prefix="FRAME" uservalue="yes">
<description>&lt;b&gt;FRAME&lt;/b&gt;&lt;p&gt;
LETTER landscape</description>
<gates>
<gate name="G$1" symbol="LETTER_L" x="0" y="0"/>
<gate name="G$2" symbol="DOCFIELD" x="147.32" y="0" addlevel="must"/>
</gates>
<devices>
<device name="">
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="special">
<description>&lt;b&gt;Special Devices&lt;/b&gt;&lt;p&gt;
7-segment displays, switches, heatsinks, crystals, transformers, etc.&lt;p&gt;
&lt;author&gt;Created by librarian@cadsoft.de&lt;/author&gt;</description>
<packages>
<package name="BATTERY">
<description>&lt;B&gt;BATTERY&lt;/B&gt;&lt;p&gt;
22 mm</description>
<wire x1="0.635" y1="2.54" x2="0.635" y2="0" width="0.1524" layer="21"/>
<wire x1="-2.54" y1="0" x2="-0.635" y2="0" width="0.1524" layer="21"/>
<wire x1="0.635" y1="0" x2="2.54" y2="0" width="0.1524" layer="21"/>
<wire x1="0.635" y1="0" x2="0.635" y2="-2.54" width="0.1524" layer="21"/>
<wire x1="1.27" y1="-3.175" x2="2.54" y2="-3.175" width="0.1524" layer="21"/>
<wire x1="1.905" y1="-2.54" x2="1.905" y2="-3.81" width="0.1524" layer="21"/>
<circle x="0" y="0" radius="11.43" width="0.1524" layer="21"/>
<circle x="0" y="0" radius="10.2362" width="0.1524" layer="21"/>
<pad name="-" x="-5.715" y="0" drill="1.016" shape="long"/>
<pad name="+" x="9.525" y="-5.08" drill="1.016" shape="long"/>
<pad name="+@1" x="9.525" y="5.08" drill="1.016" shape="long"/>
<text x="-4.1656" y="6.35" size="1.778" layer="25" ratio="10">&gt;NAME</text>
<text x="-4.445" y="3.81" size="1.778" layer="27" ratio="10">&gt;VALUE</text>
<rectangle x1="-0.635" y1="-1.27" x2="0" y2="1.27" layer="21"/>
</package>
<package name="FUSE">
<description>&lt;B&gt;FUSE&lt;/B&gt;&lt;p&gt;
5 x 20 mm</description>
<wire x1="-11.43" y1="1.905" x2="-12.7" y2="1.905" width="0.1524" layer="21"/>
<wire x1="-12.7" y1="-1.905" x2="-12.7" y2="1.905" width="0.1524" layer="21"/>
<wire x1="-12.7" y1="-1.905" x2="-11.43" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="-10.795" y1="2.54" x2="-10.795" y2="3.81" width="0.1524" layer="21"/>
<wire x1="-10.795" y1="3.81" x2="-6.985" y2="3.81" width="0.1524" layer="21"/>
<wire x1="-6.985" y1="2.54" x2="-6.985" y2="3.81" width="0.1524" layer="21"/>
<wire x1="-10.795" y1="-2.54" x2="-10.795" y2="-3.81" width="0.1524" layer="21"/>
<wire x1="-6.985" y1="-3.81" x2="-10.795" y2="-3.81" width="0.1524" layer="21"/>
<wire x1="-6.985" y1="-3.81" x2="-6.985" y2="-2.54" width="0.1524" layer="21"/>
<wire x1="-6.35" y1="1.905" x2="-5.08" y2="1.905" width="0.1524" layer="21"/>
<wire x1="-5.08" y1="1.905" x2="-5.08" y2="1.524" width="0.1524" layer="21"/>
<wire x1="-5.08" y1="-1.905" x2="-6.35" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="6.35" y1="1.905" x2="5.08" y2="1.905" width="0.1524" layer="21"/>
<wire x1="5.08" y1="-1.905" x2="5.08" y2="-1.524" width="0.1524" layer="21"/>
<wire x1="5.08" y1="-1.905" x2="6.35" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="6.985" y1="2.54" x2="6.985" y2="3.81" width="0.1524" layer="21"/>
<wire x1="6.985" y1="3.81" x2="10.795" y2="3.81" width="0.1524" layer="21"/>
<wire x1="10.795" y1="2.54" x2="10.795" y2="3.81" width="0.1524" layer="21"/>
<wire x1="6.985" y1="-2.54" x2="6.985" y2="-3.81" width="0.1524" layer="21"/>
<wire x1="10.795" y1="-3.81" x2="6.985" y2="-3.81" width="0.1524" layer="21"/>
<wire x1="10.795" y1="-3.81" x2="10.795" y2="-2.54" width="0.1524" layer="21"/>
<wire x1="11.43" y1="1.905" x2="12.7" y2="1.905" width="0.1524" layer="21"/>
<wire x1="12.7" y1="1.905" x2="12.7" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="12.7" y1="-1.905" x2="11.43" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="-5.715" y1="2.794" x2="5.715" y2="2.794" width="0.1524" layer="21"/>
<wire x1="-5.715" y1="-2.794" x2="5.715" y2="-2.794" width="0.1524" layer="21"/>
<wire x1="-5.08" y1="1.524" x2="5.08" y2="-1.524" width="0.1524" layer="21"/>
<wire x1="-5.08" y1="1.524" x2="-5.08" y2="-1.905" width="0.1524" layer="21"/>
<wire x1="5.08" y1="-1.524" x2="5.08" y2="1.905" width="0.1524" layer="21"/>
<circle x="0" y="0" radius="0.127" width="0.1524" layer="21"/>
<pad name="1" x="-11.43" y="0" drill="1.3208" shape="long"/>
<pad name="2" x="11.43" y="0" drill="1.3208" shape="long"/>
<text x="-5.08" y="3.302" size="1.778" layer="25" ratio="10">&gt;NAME</text>
<text x="-5.08" y="-5.08" size="1.778" layer="27" ratio="10">&gt;VALUE</text>
<rectangle x1="-12.065" y1="1.905" x2="-10.795" y2="3.175" layer="21"/>
<rectangle x1="-12.065" y1="-3.175" x2="-10.795" y2="-1.905" layer="21"/>
<rectangle x1="-11.43" y1="-2.54" x2="-10.795" y2="2.54" layer="51"/>
<rectangle x1="-6.985" y1="1.905" x2="-5.715" y2="3.175" layer="21"/>
<rectangle x1="-6.985" y1="-3.175" x2="-5.715" y2="-1.905" layer="21"/>
<rectangle x1="-6.985" y1="-2.54" x2="-6.35" y2="2.54" layer="21"/>
<rectangle x1="-10.795" y1="0.762" x2="-6.985" y2="2.54" layer="21"/>
<rectangle x1="-10.795" y1="-2.54" x2="-6.985" y2="-0.762" layer="21"/>
<rectangle x1="5.715" y1="1.905" x2="6.985" y2="3.175" layer="21"/>
<rectangle x1="5.715" y1="-3.175" x2="6.985" y2="-1.905" layer="21"/>
<rectangle x1="6.35" y1="-2.54" x2="6.985" y2="2.54" layer="21"/>
<rectangle x1="10.795" y1="1.905" x2="12.065" y2="3.175" layer="21"/>
<rectangle x1="10.795" y1="-3.175" x2="12.065" y2="-1.905" layer="21"/>
<rectangle x1="10.795" y1="-2.54" x2="11.43" y2="2.54" layer="51"/>
<rectangle x1="6.985" y1="0.762" x2="10.795" y2="2.54" layer="21"/>
<rectangle x1="6.985" y1="-2.54" x2="10.795" y2="-0.762" layer="21"/>
</package>
</packages>
<symbols>
<symbol name="BATTERY">
<wire x1="-1.27" y1="3.81" x2="-1.27" y2="-3.81" width="0.4064" layer="94"/>
<wire x1="0" y1="1.27" x2="0" y2="-1.27" width="0.4064" layer="94"/>
<wire x1="1.27" y1="3.81" x2="1.27" y2="-3.81" width="0.4064" layer="94"/>
<wire x1="2.54" y1="1.27" x2="2.54" y2="-1.27" width="0.4064" layer="94"/>
<wire x1="-2.54" y1="0" x2="-1.524" y2="0" width="0.1524" layer="94"/>
<text x="-3.81" y="5.08" size="1.778" layer="95">&gt;NAME</text>
<text x="-3.81" y="-6.35" size="1.778" layer="96">&gt;VALUE</text>
<pin name="-" x="5.08" y="0" visible="off" length="short" direction="pwr" rot="R180"/>
<pin name="+" x="-5.08" y="0" visible="off" length="short" direction="pwr"/>
<pin name="+@1" x="-2.54" y="0" visible="off" length="short" direction="pwr" rot="R180"/>
</symbol>
<symbol name="FUSE">
<wire x1="-5.08" y1="0" x2="-3.556" y2="1.524" width="0.254" layer="94"/>
<wire x1="0" y1="-1.524" x2="-2.54" y2="1.524" width="0.254" layer="94"/>
<wire x1="0.889" y1="-1.4986" x2="2.4892" y2="0" width="0.254" layer="94"/>
<wire x1="-3.5992" y1="1.4912" x2="-3.048" y2="1.7272" width="0.254" layer="94" curve="-46.337037" cap="flat"/>
<wire x1="-3.048" y1="1.7272" x2="-2.496" y2="1.491" width="0.254" layer="94" curve="-46.403624" cap="flat"/>
<wire x1="0.4572" y1="-1.778" x2="0.8965" y2="-1.4765" width="0.254" layer="94" curve="63.169357" cap="flat"/>
<wire x1="-0.0178" y1="-1.508" x2="0.4572" y2="-1.7778" width="0.254" layer="94" curve="64.986119" cap="flat"/>
<text x="-5.08" y="2.54" size="1.778" layer="95">&gt;NAME</text>
<text x="-5.08" y="-3.81" size="1.778" layer="96">&gt;VALUE</text>
<pin name="1" x="-7.62" y="0" visible="off" length="short" direction="pas" function="dot" swaplevel="1"/>
<pin name="2" x="5.08" y="0" visible="off" length="short" direction="pas" function="dot" swaplevel="1" rot="R180"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="BATTERY" prefix="BAT" uservalue="yes">
<description>&lt;B&gt;BATTERY&lt;/B&gt;</description>
<gates>
<gate name="G$1" symbol="BATTERY" x="0" y="0"/>
</gates>
<devices>
<device name="" package="BATTERY">
<connects>
<connect gate="G$1" pin="+" pad="+"/>
<connect gate="G$1" pin="+@1" pad="+@1"/>
<connect gate="G$1" pin="-" pad="-"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="FUSE" prefix="F" uservalue="yes">
<description>&lt;B&gt;FUSE&lt;/B&gt;&lt;p&gt;
5 x 20 mm</description>
<gates>
<gate name="G$1" symbol="FUSE" x="12.7" y="0"/>
</gates>
<devices>
<device name="" package="FUSE">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="2" pad="2"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="relay">
<description>&lt;b&gt;Relays&lt;/b&gt;&lt;p&gt;
&lt;ul&gt;
&lt;li&gt;Eichhoff
&lt;li&gt;Finder
&lt;li&gt;Fujitsu
&lt;li&gt;HAMLIN
&lt;li&gt;OMRON
&lt;li&gt;Matsushita
&lt;li&gt;NAiS
&lt;li&gt;Siemens
&lt;li&gt;Schrack
&lt;/ul&gt;
&lt;author&gt;Created by librarian@cadsoft.de&lt;/author&gt;</description>
<packages>
<package name="G2R">
<description>&lt;b&gt;RELAY&lt;/b&gt;&lt;p&gt;
1 x switch, Omron</description>
<wire x1="-4.699" y1="-6.604" x2="24.384" y2="-6.604" width="0.1524" layer="21"/>
<wire x1="24.384" y1="6.477" x2="24.384" y2="-6.604" width="0.1524" layer="21"/>
<wire x1="24.384" y1="6.477" x2="-4.699" y2="6.477" width="0.1524" layer="21"/>
<wire x1="-4.699" y1="-6.604" x2="-4.699" y2="6.477" width="0.1524" layer="21"/>
<wire x1="-2.54" y1="2.0574" x2="-2.54" y2="1.1938" width="0.1524" layer="21"/>
<wire x1="-0.6604" y1="1.1938" x2="-0.6604" y2="-1.3208" width="0.254" layer="21"/>
<wire x1="-4.4196" y1="-1.3208" x2="-4.4196" y2="1.1938" width="0.254" layer="21"/>
<wire x1="-4.4196" y1="1.1938" x2="-2.54" y2="1.1938" width="0.254" layer="21"/>
<wire x1="-2.54" y1="1.1938" x2="-1.2954" y2="1.1938" width="0.254" layer="21"/>
<wire x1="-3.7846" y1="-1.3208" x2="-4.4196" y2="-1.3208" width="0.254" layer="21"/>
<wire x1="-1.2954" y1="1.1938" x2="-3.7846" y2="-1.3208" width="0.1524" layer="21"/>
<wire x1="-1.2954" y1="1.1938" x2="-0.6604" y2="1.1938" width="0.254" layer="21"/>
<wire x1="-0.6604" y1="-1.3208" x2="-2.54" y2="-1.3208" width="0.254" layer="21"/>
<wire x1="-2.54" y1="-1.3208" x2="-2.54" y2="-1.9304" width="0.1524" layer="21"/>
<wire x1="-2.54" y1="-1.3208" x2="-3.7846" y2="-1.3208" width="0.254" layer="21"/>
<wire x1="16.256" y1="-0.508" x2="16.5862" y2="-0.1778" width="0.254" layer="21"/>
<wire x1="16.5862" y1="-0.1778" x2="13.97" y2="-0.1778" width="0.1524" layer="21"/>
<wire x1="16.5862" y1="-0.1778" x2="17.526" y2="0.762" width="0.254" layer="21"/>
<wire x1="13.97" y1="-0.1778" x2="13.97" y2="-1.8288" width="0.1524" layer="21"/>
<wire x1="18.4912" y1="-0.1778" x2="20.955" y2="-0.1778" width="0.1524" layer="21"/>
<wire x1="20.955" y1="-0.1778" x2="20.955" y2="-1.8288" width="0.1524" layer="21"/>
<wire x1="17.526" y1="1.905" x2="17.526" y2="0.762" width="0.1524" layer="21"/>
<pad name="2" x="-2.54" y="3.81" drill="1.3208" shape="long"/>
<pad name="1" x="-2.54" y="-3.683" drill="1.3208" shape="long"/>
<pad name="P" x="17.4498" y="3.81" drill="1.3208" shape="long"/>
<pad name="O" x="13.97" y="-3.683" drill="1.3208" shape="long"/>
<pad name="S" x="20.955" y="-3.683" drill="1.3208" shape="long"/>
<text x="26.6446" y="-6.2992" size="1.778" layer="25" ratio="10" rot="R90">&gt;NAME</text>
<text x="3.81" y="-5.08" size="1.778" layer="27" ratio="10" rot="R90">&gt;VALUE</text>
</package>
</packages>
<symbols>
<symbol name="K">
<wire x1="-3.81" y1="-1.905" x2="-1.905" y2="-1.905" width="0.254" layer="94"/>
<wire x1="3.81" y1="-1.905" x2="3.81" y2="1.905" width="0.254" layer="94"/>
<wire x1="3.81" y1="1.905" x2="1.905" y2="1.905" width="0.254" layer="94"/>
<wire x1="-3.81" y1="1.905" x2="-3.81" y2="-1.905" width="0.254" layer="94"/>
<wire x1="0" y1="-2.54" x2="0" y2="-1.905" width="0.1524" layer="94"/>
<wire x1="0" y1="-1.905" x2="3.81" y2="-1.905" width="0.254" layer="94"/>
<wire x1="0" y1="2.54" x2="0" y2="1.905" width="0.1524" layer="94"/>
<wire x1="0" y1="1.905" x2="-3.81" y2="1.905" width="0.254" layer="94"/>
<wire x1="-1.905" y1="-1.905" x2="1.905" y2="1.905" width="0.1524" layer="94"/>
<wire x1="-1.905" y1="-1.905" x2="0" y2="-1.905" width="0.254" layer="94"/>
<wire x1="1.905" y1="1.905" x2="0" y2="1.905" width="0.254" layer="94"/>
<text x="1.27" y="2.921" size="1.778" layer="96">&gt;VALUE</text>
<text x="1.27" y="5.08" size="1.778" layer="95">&gt;PART</text>
<pin name="2" x="0" y="-5.08" visible="pad" length="short" direction="pas" rot="R90"/>
<pin name="1" x="0" y="5.08" visible="pad" length="short" direction="pas" rot="R270"/>
</symbol>
<symbol name="U">
<wire x1="3.175" y1="5.08" x2="1.905" y2="5.08" width="0.254" layer="94"/>
<wire x1="-3.175" y1="5.08" x2="-1.905" y2="5.08" width="0.254" layer="94"/>
<wire x1="0" y1="1.27" x2="2.54" y2="5.715" width="0.254" layer="94"/>
<wire x1="0" y1="1.27" x2="0" y2="0" width="0.254" layer="94"/>
<circle x="0" y="1.27" radius="0.127" width="0.4064" layer="94"/>
<text x="2.54" y="0" size="1.778" layer="95">&gt;PART</text>
<pin name="O" x="5.08" y="5.08" visible="pad" length="short" direction="pas" rot="R180"/>
<pin name="S" x="-5.08" y="5.08" visible="pad" length="short" direction="pas"/>
<pin name="P" x="0" y="-2.54" visible="pad" length="short" direction="pas" rot="R90"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="G2R" prefix="K">
<description>&lt;b&gt;RELAY&lt;/b&gt;&lt;p&gt;
1 x switch, Omron</description>
<gates>
<gate name="1" symbol="K" x="0" y="0" addlevel="must"/>
<gate name="2" symbol="U" x="17.78" y="0" addlevel="always"/>
</gates>
<devices>
<device name="" package="G2R">
<connects>
<connect gate="1" pin="1" pad="1"/>
<connect gate="1" pin="2" pad="2"/>
<connect gate="2" pin="O" pad="O"/>
<connect gate="2" pin="P" pad="P"/>
<connect gate="2" pin="S" pad="S"/>
</connects>
<technologies>
<technology name="">
<attribute name="MF" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OC_FARNELL" value="1569185" constant="no"/>
<attribute name="OC_NEWARK" value="unknown" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="switch-omron">
<description>&lt;b&gt;Omron Switches&lt;/b&gt;&lt;p&gt;
&lt;author&gt;Created by librarian@cadsoft.de&lt;/author&gt;</description>
<packages>
</packages>
<symbols>
<symbol name="D-TS">
<wire x1="0" y1="-3.175" x2="0" y2="-2.54" width="0.254" layer="95"/>
<wire x1="0" y1="2.54" x2="0" y2="3.175" width="0.254" layer="95"/>
<wire x1="0" y1="-2.54" x2="-0.635" y2="0" width="0.254" layer="95"/>
<wire x1="-4.445" y1="1.905" x2="-3.175" y2="1.905" width="0.254" layer="95"/>
<wire x1="-4.445" y1="1.905" x2="-4.445" y2="0" width="0.254" layer="95"/>
<wire x1="-4.445" y1="-1.905" x2="-3.175" y2="-1.905" width="0.254" layer="95"/>
<wire x1="-4.445" y1="0" x2="-3.175" y2="0" width="0.1524" layer="95"/>
<wire x1="-4.445" y1="0" x2="-4.445" y2="-1.905" width="0.254" layer="95"/>
<wire x1="-2.54" y1="0" x2="-1.905" y2="0" width="0.1524" layer="95"/>
<wire x1="-1.27" y1="0" x2="-0.635" y2="0" width="0.1524" layer="95"/>
<wire x1="-0.635" y1="0" x2="-1.27" y2="2.54" width="0.254" layer="95"/>
<wire x1="0" y1="-3.175" x2="0" y2="-5.08" width="0.1524" layer="95"/>
<wire x1="0" y1="3.175" x2="0" y2="5.08" width="0.1524" layer="95"/>
<text x="-6.35" y="-1.905" size="1.778" layer="95" rot="R90">&gt;NAME</text>
<text x="-3.81" y="3.175" size="1.778" layer="96" rot="R90">&gt;VALUE</text>
</symbol>
</symbols>
<devicesets>
<deviceset name="D-TS" prefix="S" uservalue="yes">
<description>&lt;b&gt;SWITCH&lt;/b&gt;</description>
<gates>
<gate name="G$1" symbol="D-TS" x="0" y="0"/>
</gates>
<devices>
<device name="">
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="con-molex">
<description>&lt;b&gt;Molex Connectors&lt;/b&gt;&lt;p&gt;
&lt;author&gt;Created by librarian@cadsoft.de&lt;/author&gt;</description>
<packages>
<package name="70543-02">
<description>&lt;b&gt;C-Grid SL Connector&lt;/b&gt;&lt;p&gt;
 vertical, 2 pin</description>
<wire x1="3.81" y1="-2.8575" x2="3.81" y2="2.8575" width="0.254" layer="21"/>
<wire x1="3.81" y1="2.8575" x2="-3.81" y2="2.8575" width="0.254" layer="21"/>
<wire x1="-3.81" y1="2.8575" x2="-3.81" y2="-2.8575" width="0.254" layer="21"/>
<wire x1="-3.81" y1="-2.8575" x2="-3.4925" y2="-2.8575" width="0.254" layer="21"/>
<wire x1="-3.4925" y1="-2.8575" x2="-3.4925" y2="-3.81" width="0.254" layer="21"/>
<wire x1="-3.4925" y1="-3.81" x2="3.4925" y2="-3.81" width="0.254" layer="21"/>
<wire x1="3.4925" y1="-3.81" x2="3.4925" y2="-2.8575" width="0.254" layer="21"/>
<wire x1="3.4925" y1="-2.8575" x2="3.81" y2="-2.8575" width="0.254" layer="21"/>
<wire x1="-3.175" y1="2.2225" x2="-3.175" y2="-2.2225" width="0.0508" layer="51"/>
<wire x1="3.175" y1="2.2225" x2="3.175" y2="-2.2225" width="0.0508" layer="51"/>
<wire x1="-3.175" y1="2.2225" x2="3.175" y2="2.2225" width="0.0508" layer="51"/>
<wire x1="-3.175" y1="-2.2225" x2="-2.8575" y2="-2.2225" width="0.0508" layer="51"/>
<wire x1="-2.8575" y1="-2.2225" x2="2.8575" y2="-2.2225" width="0.0508" layer="51"/>
<wire x1="2.8575" y1="-2.2225" x2="3.175" y2="-2.2225" width="0.0508" layer="51"/>
<wire x1="2.8575" y1="-3.175" x2="-2.8575" y2="-3.175" width="0.0508" layer="51"/>
<wire x1="-2.8575" y1="-2.2225" x2="-2.8575" y2="-3.175" width="0.0508" layer="51"/>
<wire x1="2.8575" y1="-2.2225" x2="2.8575" y2="-3.175" width="0.0508" layer="51"/>
<pad name="2" x="1.27" y="0" drill="1.016" shape="long" rot="R90"/>
<pad name="1" x="-1.27" y="0" drill="1.016" shape="long" rot="R90"/>
<text x="-4.445" y="-2.54" size="1.016" layer="25" ratio="10" rot="R90">&gt;NAME</text>
<text x="-3.4925" y="3.4925" size="0.8128" layer="27" ratio="10">&gt;VALUE</text>
<text x="-2.8575" y="-1.5875" size="1.016" layer="51" ratio="10">1</text>
<rectangle x1="1.0319" y1="-0.2381" x2="1.5081" y2="0.2381" layer="51"/>
<rectangle x1="-1.5081" y1="-0.2381" x2="-1.0319" y2="0.2381" layer="51"/>
</package>
<package name="70553-02">
<description>&lt;b&gt;C-Grid SL Connector&lt;/b&gt;&lt;p&gt;
 right angle, 2 pin</description>
<wire x1="3.9688" y1="5.8738" x2="-3.9688" y2="5.8738" width="0.254" layer="21"/>
<wire x1="-1.27" y1="2.54" x2="-1.27" y2="-3.175" width="0.254" layer="21"/>
<wire x1="-1.27" y1="-3.175" x2="1.27" y2="-3.175" width="0.254" layer="21"/>
<wire x1="1.27" y1="-3.175" x2="1.27" y2="2.54" width="0.254" layer="21"/>
<wire x1="-3.9688" y1="5.8738" x2="-3.9688" y2="2.54" width="0.254" layer="21"/>
<wire x1="-3.9688" y1="2.54" x2="-3.175" y2="2.54" width="0.254" layer="21"/>
<wire x1="-3.175" y1="2.54" x2="-1.27" y2="2.54" width="0.254" layer="21"/>
<wire x1="1.27" y1="2.54" x2="3.175" y2="2.54" width="0.254" layer="21"/>
<wire x1="3.175" y1="2.54" x2="3.9688" y2="2.54" width="0.254" layer="21"/>
<wire x1="3.9688" y1="2.54" x2="3.9688" y2="5.8738" width="0.254" layer="21"/>
<wire x1="-3.175" y1="2.54" x2="-3.175" y2="3.175" width="0.254" layer="21"/>
<wire x1="-3.175" y1="3.175" x2="-1.905" y2="4.445" width="0.254" layer="21" curve="-90"/>
<wire x1="-1.905" y1="4.445" x2="1.905" y2="4.445" width="0.254" layer="21"/>
<wire x1="1.905" y1="4.445" x2="3.175" y2="3.175" width="0.254" layer="21" curve="-90"/>
<wire x1="3.175" y1="3.175" x2="3.175" y2="2.54" width="0.254" layer="21"/>
<wire x1="-3.9688" y1="2.54" x2="-3.9688" y2="-5.715" width="0.254" layer="21"/>
<wire x1="-3.9688" y1="-5.715" x2="3.9688" y2="-5.715" width="0.254" layer="21"/>
<wire x1="3.9688" y1="-5.715" x2="3.9688" y2="2.54" width="0.254" layer="21"/>
<wire x1="-2.8575" y1="-5.715" x2="-2.8575" y2="-6.35" width="0.254" layer="51"/>
<wire x1="-2.8575" y1="-6.35" x2="-2.8575" y2="-7.9375" width="0.254" layer="51"/>
<wire x1="2.8575" y1="-7.9375" x2="2.8575" y2="-6.35" width="0.254" layer="51"/>
<wire x1="2.8575" y1="-6.35" x2="2.8575" y2="-5.715" width="0.254" layer="51"/>
<wire x1="-2.8575" y1="-6.35" x2="-1.905" y2="-6.35" width="0.254" layer="51"/>
<wire x1="-1.905" y1="-6.35" x2="-0.635" y2="-6.35" width="0.127" layer="51"/>
<wire x1="-0.635" y1="-6.35" x2="0.635" y2="-6.35" width="0.254" layer="51"/>
<wire x1="0.635" y1="-6.35" x2="1.905" y2="-6.35" width="0.127" layer="51"/>
<wire x1="1.905" y1="-6.35" x2="2.8575" y2="-6.35" width="0.254" layer="51"/>
<wire x1="-1.905" y1="-6.35" x2="-1.905" y2="-7.6835" width="0.254" layer="51"/>
<wire x1="-1.905" y1="-7.6835" x2="-2.159" y2="-7.9375" width="0.254" layer="51" curve="-90"/>
<wire x1="-2.159" y1="-7.9375" x2="-2.8575" y2="-7.9375" width="0.254" layer="51"/>
<wire x1="-0.635" y1="-6.35" x2="-0.635" y2="-7.6835" width="0.254" layer="51"/>
<wire x1="-0.635" y1="-7.6835" x2="-0.381" y2="-7.9375" width="0.254" layer="51" curve="90"/>
<wire x1="0.635" y1="-6.35" x2="0.635" y2="-7.6835" width="0.254" layer="51"/>
<wire x1="0.635" y1="-7.6835" x2="0.381" y2="-7.9375" width="0.254" layer="51" curve="-90"/>
<wire x1="0.381" y1="-7.9375" x2="-0.381" y2="-7.9375" width="0.254" layer="51"/>
<wire x1="1.905" y1="-6.35" x2="1.905" y2="-7.6835" width="0.254" layer="51"/>
<wire x1="1.905" y1="-7.6835" x2="2.159" y2="-7.9375" width="0.254" layer="51" curve="90"/>
<wire x1="2.159" y1="-7.9375" x2="2.8575" y2="-7.9375" width="0.254" layer="51"/>
<pad name="2" x="1.27" y="-7.62" drill="1.0922" shape="long" rot="R90"/>
<pad name="1" x="-1.27" y="-7.62" drill="1.0922" shape="long" rot="R90"/>
<text x="-4.445" y="-5.715" size="1.016" layer="25" ratio="10" rot="R90">&gt;NAME</text>
<text x="5.715" y="-5.715" size="0.8128" layer="27" ratio="10" rot="R90">&gt;VALUE</text>
<rectangle x1="-1.5875" y1="-7.62" x2="-0.9525" y2="-6.35" layer="51"/>
<rectangle x1="0.9525" y1="-7.62" x2="1.5875" y2="-6.35" layer="51"/>
<polygon width="0.0508" layer="21">
<vertex x="-3.81" y="5.8738"/>
<vertex x="-3.3338" y="3.9689"/>
<vertex x="-2.8575" y="5.8738"/>
</polygon>
</package>
<package name="15-91-02">
<description>&lt;b&gt;C-Grid SL Connector&lt;/b&gt;&lt;p&gt;
 right angle SMD, 2 pin</description>
<wire x1="3.9688" y1="5.08" x2="-3.9688" y2="5.08" width="0.254" layer="21"/>
<wire x1="-1.27" y1="1.905" x2="-1.27" y2="-3.81" width="0.254" layer="51"/>
<wire x1="-1.27" y1="-3.81" x2="1.27" y2="-3.81" width="0.254" layer="51"/>
<wire x1="1.27" y1="-3.81" x2="1.27" y2="1.905" width="0.254" layer="51"/>
<wire x1="-3.9688" y1="5.08" x2="-3.9688" y2="2.2225" width="0.254" layer="21"/>
<wire x1="-3.9688" y1="2.2225" x2="-3.9688" y2="1.905" width="0.254" layer="51"/>
<wire x1="-3.9688" y1="1.905" x2="-3.175" y2="1.905" width="0.254" layer="51"/>
<wire x1="-3.175" y1="1.905" x2="-1.27" y2="1.905" width="0.254" layer="51"/>
<wire x1="1.27" y1="1.905" x2="3.175" y2="1.905" width="0.254" layer="51"/>
<wire x1="3.175" y1="1.905" x2="3.9688" y2="1.905" width="0.254" layer="51"/>
<wire x1="3.9688" y1="1.905" x2="3.9688" y2="2.2225" width="0.254" layer="51"/>
<wire x1="3.9688" y1="2.2225" x2="3.9688" y2="5.08" width="0.254" layer="21"/>
<wire x1="-3.175" y1="1.905" x2="-3.175" y2="2.54" width="0.254" layer="51"/>
<wire x1="-3.175" y1="2.54" x2="-1.905" y2="3.81" width="0.254" layer="51" curve="-90"/>
<wire x1="-1.905" y1="3.81" x2="1.905" y2="3.81" width="0.254" layer="51"/>
<wire x1="1.905" y1="3.81" x2="3.175" y2="2.54" width="0.254" layer="51" curve="-90"/>
<wire x1="3.175" y1="2.54" x2="3.175" y2="1.905" width="0.254" layer="51"/>
<wire x1="-3.9688" y1="-0.635" x2="-3.9688" y2="-6.35" width="0.254" layer="21"/>
<wire x1="-3.9688" y1="-6.35" x2="3.9688" y2="-6.35" width="0.254" layer="21"/>
<wire x1="3.9688" y1="-6.35" x2="3.9688" y2="-0.635" width="0.254" layer="21"/>
<wire x1="-2.54" y1="-6.35" x2="-2.54" y2="-8.5725" width="0.254" layer="51"/>
<wire x1="2.54" y1="-8.5725" x2="2.54" y2="-6.35" width="0.254" layer="51"/>
<wire x1="-2.54" y1="-6.985" x2="-1.905" y2="-6.985" width="0.254" layer="51"/>
<wire x1="-0.635" y1="-6.985" x2="0.635" y2="-6.985" width="0.254" layer="51"/>
<wire x1="1.905" y1="-6.985" x2="2.54" y2="-6.985" width="0.254" layer="51"/>
<wire x1="-1.905" y1="-6.985" x2="-1.905" y2="-8.3185" width="0.254" layer="51"/>
<wire x1="-1.905" y1="-8.3185" x2="-2.159" y2="-8.5725" width="0.254" layer="51" curve="-90"/>
<wire x1="-2.159" y1="-8.5725" x2="-2.54" y2="-8.5725" width="0.254" layer="51"/>
<wire x1="0.635" y1="-6.985" x2="0.635" y2="-8.3185" width="0.254" layer="51"/>
<wire x1="0.635" y1="-8.3185" x2="0.381" y2="-8.5725" width="0.254" layer="51" curve="-90"/>
<wire x1="0.381" y1="-8.5725" x2="-0.381" y2="-8.5725" width="0.254" layer="51"/>
<wire x1="-0.381" y1="-8.5725" x2="-0.635" y2="-8.3185" width="0.254" layer="51" curve="-90"/>
<wire x1="-0.635" y1="-8.3185" x2="-0.635" y2="-6.985" width="0.254" layer="51"/>
<wire x1="1.905" y1="-6.985" x2="1.905" y2="-8.3185" width="0.254" layer="51"/>
<wire x1="1.905" y1="-8.3185" x2="2.159" y2="-8.5725" width="0.254" layer="51" curve="90"/>
<wire x1="2.159" y1="-8.5725" x2="2.54" y2="-8.5725" width="0.254" layer="51"/>
<wire x1="-3.9688" y1="-0.635" x2="-3.9688" y2="1.905" width="0.254" layer="51"/>
<wire x1="3.9688" y1="-0.635" x2="3.9688" y2="1.905" width="0.254" layer="51"/>
<wire x1="-1.905" y1="-6.985" x2="-0.635" y2="-6.985" width="0.254" layer="51"/>
<wire x1="0.635" y1="-6.985" x2="1.905" y2="-6.985" width="0.254" layer="51"/>
<smd name="1" x="-1.27" y="-10.795" dx="5.334" dy="1.651" layer="1" rot="R90"/>
<smd name="2" x="1.27" y="-10.795" dx="5.334" dy="1.651" layer="1" rot="R90"/>
<text x="-4.445" y="-6.35" size="1.016" layer="25" ratio="10" rot="R90">&gt;NAME</text>
<text x="5.715" y="-6.35" size="0.8128" layer="27" ratio="10" rot="R90">&gt;VALUE</text>
<rectangle x1="-1.5875" y1="-10.795" x2="-0.9525" y2="-6.985" layer="51"/>
<rectangle x1="0.9525" y1="-10.795" x2="1.5875" y2="-6.985" layer="51"/>
<hole x="-2.667" y="0.8382" drill="3.4036"/>
<hole x="2.667" y="0.8382" drill="3.4036"/>
<polygon width="0.2032" layer="21">
<vertex x="-3.81" y="5.08"/>
<vertex x="-3.3337" y="3.4926"/>
<vertex x="-2.8575" y="5.08"/>
</polygon>
</package>
</packages>
<symbols>
<symbol name="M">
<wire x1="1.27" y1="0" x2="0" y2="0" width="0.6096" layer="94"/>
<text x="2.54" y="-0.762" size="1.524" layer="95">&gt;NAME</text>
<pin name="S" x="-2.54" y="0" visible="off" length="short" direction="pas"/>
</symbol>
<symbol name="MV">
<wire x1="1.27" y1="0" x2="0" y2="0" width="0.6096" layer="94"/>
<text x="2.54" y="-0.762" size="1.524" layer="95">&gt;NAME</text>
<text x="-0.762" y="1.397" size="1.778" layer="96">&gt;VALUE</text>
<pin name="S" x="-2.54" y="0" visible="off" length="short" direction="pas"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="C-GRID-02" prefix="X">
<description>&lt;b&gt;CONNECTOR&lt;/b&gt;&lt;p&gt;
wire to board 2.54 mm (0.100") pitch header</description>
<gates>
<gate name="-2" symbol="M" x="2.54" y="15.24" addlevel="always" swaplevel="1"/>
<gate name="-1" symbol="MV" x="2.54" y="17.78" addlevel="always" swaplevel="1"/>
</gates>
<devices>
<device name="-70543" package="70543-02">
<connects>
<connect gate="-1" pin="S" pad="1"/>
<connect gate="-2" pin="S" pad="2"/>
</connects>
<technologies>
<technology name="">
<attribute name="MF" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OC_FARNELL" value="unknown" constant="no"/>
<attribute name="OC_NEWARK" value="unknown" constant="no"/>
</technology>
</technologies>
</device>
<device name="-70553" package="70553-02">
<connects>
<connect gate="-1" pin="S" pad="1"/>
<connect gate="-2" pin="S" pad="2"/>
</connects>
<technologies>
<technology name="">
<attribute name="MF" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OC_FARNELL" value="unknown" constant="no"/>
<attribute name="OC_NEWARK" value="unknown" constant="no"/>
</technology>
</technologies>
</device>
<device name="-15-19" package="15-91-02">
<connects>
<connect gate="-1" pin="S" pad="1"/>
<connect gate="-2" pin="S" pad="2"/>
</connects>
<technologies>
<technology name="">
<attribute name="MF" value="" constant="no"/>
<attribute name="MPN" value="" constant="no"/>
<attribute name="OC_FARNELL" value="unknown" constant="no"/>
<attribute name="OC_NEWARK" value="unknown" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0" drill="0">
</class>
</classes>
<parts>
<part name="FRAME1" library="frames" deviceset="LETTER_L" device=""/>
<part name="BAT1" library="special" deviceset="BATTERY" device="" value="12V, 22Ah"/>
<part name="BAT2" library="special" deviceset="BATTERY" device="" value="12V, 22Ah"/>
<part name="F1" library="special" deviceset="FUSE" device="" value="80A"/>
<part name="F2" library="special" deviceset="FUSE" device="" value="25A"/>
<part name="F3" library="special" deviceset="FUSE" device="" value="10A"/>
<part name="F4" library="special" deviceset="FUSE" device="" value="1A"/>
<part name="F5" library="special" deviceset="FUSE" device="" value="1A"/>
<part name="F6" library="special" deviceset="FUSE" device="" value="1A"/>
<part name="F7" library="special" deviceset="FUSE" device="" value="40A"/>
<part name="F8" library="special" deviceset="FUSE" device="" value="25A"/>
<part name="F9" library="special" deviceset="FUSE" device="" value="25A"/>
<part name="F10" library="special" deviceset="FUSE" device="" value="40A"/>
<part name="K1" library="relay" deviceset="G2R" device="" value="RELAY"/>
<part name="S1" library="switch-omron" deviceset="D-TS" device="" value="E-STOP"/>
<part name="CHG" library="con-molex" deviceset="C-GRID-02" device="-70543" value="SB120"/>
<part name="F11" library="special" deviceset="FUSE" device="" value="40A"/>
<part name="FRAME2" library="frames" deviceset="LETTER_L" device=""/>
</parts>
<sheets>
<sheet>
<plain>
<text x="149.86" y="25.4" size="2.54" layer="91">Team Cephal
Computing System</text>
<text x="368.3" y="86.36" size="1.778" layer="94" rot="R90">Mini-ITX
PC</text>
<text x="378.46" y="86.36" size="1.778" layer="94" rot="R90">PoE
Switch</text>
<text x="388.62" y="86.36" size="1.778" layer="94" rot="R90">Safety
Light</text>
<text x="398.78" y="86.36" size="1.778" layer="94" rot="R90">Wireless
Pause</text>
<text x="441.96" y="86.36" size="1.778" layer="94" rot="R90">Roboclaw
(Drive)</text>
<text x="452.12" y="86.36" size="1.778" layer="94" rot="R90">Roboclaw
(Collector)</text>
<text x="462.28" y="86.36" size="1.778" layer="94" rot="R90">Roboclaw
(Scoop)</text>
<wire x1="363.22" y1="99.06" x2="363.22" y2="83.82" width="0.1524" layer="94"/>
<wire x1="363.22" y1="83.82" x2="368.3" y2="83.82" width="0.1524" layer="94"/>
<wire x1="368.3" y1="83.82" x2="368.3" y2="99.06" width="0.1524" layer="94"/>
<wire x1="368.3" y1="99.06" x2="363.22" y2="99.06" width="0.1524" layer="94"/>
<wire x1="373.38" y1="99.06" x2="373.38" y2="83.82" width="0.1524" layer="94"/>
<wire x1="373.38" y1="83.82" x2="378.46" y2="83.82" width="0.1524" layer="94"/>
<wire x1="378.46" y1="83.82" x2="378.46" y2="99.06" width="0.1524" layer="94"/>
<wire x1="378.46" y1="99.06" x2="373.38" y2="99.06" width="0.1524" layer="94"/>
<wire x1="383.54" y1="99.06" x2="383.54" y2="83.82" width="0.1524" layer="94"/>
<wire x1="383.54" y1="83.82" x2="388.62" y2="83.82" width="0.1524" layer="94"/>
<wire x1="388.62" y1="83.82" x2="388.62" y2="99.06" width="0.1524" layer="94"/>
<wire x1="388.62" y1="99.06" x2="383.54" y2="99.06" width="0.1524" layer="94"/>
<wire x1="393.7" y1="99.06" x2="393.7" y2="83.82" width="0.1524" layer="94"/>
<wire x1="393.7" y1="83.82" x2="398.78" y2="83.82" width="0.1524" layer="94"/>
<wire x1="398.78" y1="83.82" x2="398.78" y2="99.06" width="0.1524" layer="94"/>
<wire x1="398.78" y1="99.06" x2="393.7" y2="99.06" width="0.1524" layer="94"/>
<wire x1="436.88" y1="99.06" x2="436.88" y2="83.82" width="0.1524" layer="94"/>
<wire x1="436.88" y1="83.82" x2="441.96" y2="83.82" width="0.1524" layer="94"/>
<wire x1="441.96" y1="83.82" x2="441.96" y2="99.06" width="0.1524" layer="94"/>
<wire x1="441.96" y1="99.06" x2="436.88" y2="99.06" width="0.1524" layer="94"/>
<wire x1="447.04" y1="99.06" x2="447.04" y2="83.82" width="0.1524" layer="94"/>
<wire x1="447.04" y1="83.82" x2="452.12" y2="83.82" width="0.1524" layer="94"/>
<wire x1="452.12" y1="83.82" x2="452.12" y2="99.06" width="0.1524" layer="94"/>
<wire x1="452.12" y1="99.06" x2="447.04" y2="99.06" width="0.1524" layer="94"/>
<wire x1="457.2" y1="99.06" x2="457.2" y2="83.82" width="0.1524" layer="94"/>
<wire x1="457.2" y1="83.82" x2="462.28" y2="83.82" width="0.1524" layer="94"/>
<wire x1="462.28" y1="83.82" x2="462.28" y2="99.06" width="0.1524" layer="94"/>
<wire x1="462.28" y1="99.06" x2="457.2" y2="99.06" width="0.1524" layer="94"/>
<wire x1="17.78" y1="177.8" x2="17.78" y2="119.38" width="0.1524" layer="94"/>
<wire x1="17.78" y1="119.38" x2="50.8" y2="119.38" width="0.1524" layer="94"/>
<wire x1="50.8" y1="119.38" x2="50.8" y2="177.8" width="0.1524" layer="94"/>
<wire x1="50.8" y1="177.8" x2="17.78" y2="177.8" width="0.1524" layer="94"/>
<text x="20.32" y="170.18" size="1.778" layer="94">Mini-ITX
PC</text>
<wire x1="88.9" y1="175.26" x2="88.9" y2="165.1" width="0.1524" layer="94"/>
<wire x1="88.9" y1="165.1" x2="132.08" y2="165.1" width="0.1524" layer="94"/>
<wire x1="132.08" y1="165.1" x2="132.08" y2="175.26" width="0.1524" layer="94"/>
<wire x1="132.08" y1="175.26" x2="88.9" y2="175.26" width="0.1524" layer="94"/>
<text x="91.44" y="167.64" size="1.778" layer="94">8 Port PoE
Gigabit Switch</text>
<wire x1="88.9" y1="127" x2="88.9" y2="114.3" width="0.1524" layer="94"/>
<wire x1="88.9" y1="114.3" x2="116.84" y2="114.3" width="0.1524" layer="94"/>
<wire x1="116.84" y1="114.3" x2="116.84" y2="127" width="0.1524" layer="94"/>
<wire x1="116.84" y1="127" x2="88.9" y2="127" width="0.1524" layer="94"/>
<text x="91.44" y="119.38" size="1.778" layer="94">LinkM
USB-&gt;I2C converter</text>
<wire x1="137.16" y1="127" x2="137.16" y2="114.3" width="0.1524" layer="94"/>
<wire x1="137.16" y1="114.3" x2="162.56" y2="114.3" width="0.1524" layer="94"/>
<wire x1="162.56" y1="114.3" x2="162.56" y2="127" width="0.1524" layer="94"/>
<wire x1="162.56" y1="127" x2="137.16" y2="127" width="0.1524" layer="94"/>
<text x="139.7" y="116.84" size="1.778" layer="94">MPU-6000
6DOF Gyro/Accel
(No Magnetometer)</text>
<wire x1="144.78" y1="167.64" x2="144.78" y2="157.48" width="0.1524" layer="94"/>
<wire x1="144.78" y1="157.48" x2="162.56" y2="157.48" width="0.1524" layer="94"/>
<wire x1="162.56" y1="157.48" x2="162.56" y2="167.64" width="0.1524" layer="94"/>
<wire x1="162.56" y1="167.64" x2="144.78" y2="167.64" width="0.1524" layer="94"/>
<text x="147.32" y="160.02" size="1.778" layer="94">Point Grey
Camera</text>
<wire x1="144.78" y1="154.94" x2="144.78" y2="144.78" width="0.1524" layer="94"/>
<wire x1="144.78" y1="144.78" x2="162.56" y2="144.78" width="0.1524" layer="94"/>
<wire x1="162.56" y1="144.78" x2="162.56" y2="154.94" width="0.1524" layer="94"/>
<wire x1="162.56" y1="154.94" x2="144.78" y2="154.94" width="0.1524" layer="94"/>
<text x="147.32" y="147.32" size="1.778" layer="94">Point Grey
Camera</text>
<wire x1="144.78" y1="142.24" x2="144.78" y2="132.08" width="0.1524" layer="94"/>
<wire x1="144.78" y1="132.08" x2="162.56" y2="132.08" width="0.1524" layer="94"/>
<wire x1="162.56" y1="132.08" x2="162.56" y2="142.24" width="0.1524" layer="94"/>
<wire x1="162.56" y1="142.24" x2="144.78" y2="142.24" width="0.1524" layer="94"/>
<text x="147.32" y="134.62" size="1.778" layer="94">Point Grey
Camera</text>
<wire x1="17.78" y1="88.9" x2="17.78" y2="66.04" width="0.1524" layer="94"/>
<wire x1="17.78" y1="66.04" x2="38.1" y2="66.04" width="0.1524" layer="94"/>
<wire x1="38.1" y1="66.04" x2="38.1" y2="88.9" width="0.1524" layer="94"/>
<wire x1="38.1" y1="88.9" x2="17.78" y2="88.9" width="0.1524" layer="94"/>
<text x="20.32" y="81.28" size="1.778" layer="94">Roboclaw 30A
(Drive)</text>
<wire x1="45.72" y1="88.9" x2="45.72" y2="66.04" width="0.1524" layer="94"/>
<wire x1="45.72" y1="66.04" x2="66.04" y2="66.04" width="0.1524" layer="94"/>
<wire x1="66.04" y1="66.04" x2="66.04" y2="88.9" width="0.1524" layer="94"/>
<wire x1="66.04" y1="88.9" x2="45.72" y2="88.9" width="0.1524" layer="94"/>
<text x="48.26" y="81.28" size="1.778" layer="94">Roboclaw 15A
(Collector)</text>
<wire x1="73.66" y1="88.9" x2="73.66" y2="66.04" width="0.1524" layer="94"/>
<wire x1="73.66" y1="66.04" x2="93.98" y2="66.04" width="0.1524" layer="94"/>
<wire x1="93.98" y1="66.04" x2="93.98" y2="88.9" width="0.1524" layer="94"/>
<wire x1="93.98" y1="88.9" x2="73.66" y2="88.9" width="0.1524" layer="94"/>
<text x="76.2" y="81.28" size="1.778" layer="94">Roboclaw 15A
(Scoop)</text>
<circle x="15.24" y="12.7" radius="7.184203125" width="0.1524" layer="94"/>
<circle x="43.18" y="12.7" radius="7.184203125" width="0.1524" layer="94"/>
<circle x="71.12" y="12.7" radius="7.184203125" width="0.1524" layer="94"/>
<circle x="99.06" y="12.7" radius="7.184203125" width="0.1524" layer="94"/>
<circle x="127" y="12.7" radius="7.184203125" width="0.1524" layer="94"/>
<wire x1="25.4" y1="25.4" x2="25.4" y2="7.62" width="0.1524" layer="94"/>
<wire x1="25.4" y1="7.62" x2="30.48" y2="7.62" width="0.1524" layer="94"/>
<wire x1="30.48" y1="7.62" x2="30.48" y2="25.4" width="0.1524" layer="94"/>
<wire x1="30.48" y1="25.4" x2="25.4" y2="25.4" width="0.1524" layer="94"/>
<wire x1="53.34" y1="25.4" x2="53.34" y2="7.62" width="0.1524" layer="94"/>
<wire x1="53.34" y1="7.62" x2="58.42" y2="7.62" width="0.1524" layer="94"/>
<wire x1="58.42" y1="7.62" x2="58.42" y2="25.4" width="0.1524" layer="94"/>
<wire x1="58.42" y1="25.4" x2="53.34" y2="25.4" width="0.1524" layer="94"/>
<wire x1="81.28" y1="25.4" x2="81.28" y2="7.62" width="0.1524" layer="94"/>
<wire x1="81.28" y1="7.62" x2="86.36" y2="7.62" width="0.1524" layer="94"/>
<wire x1="86.36" y1="7.62" x2="86.36" y2="25.4" width="0.1524" layer="94"/>
<wire x1="86.36" y1="25.4" x2="81.28" y2="25.4" width="0.1524" layer="94"/>
<wire x1="109.22" y1="25.4" x2="109.22" y2="7.62" width="0.1524" layer="94"/>
<wire x1="109.22" y1="7.62" x2="114.3" y2="7.62" width="0.1524" layer="94"/>
<wire x1="114.3" y1="7.62" x2="114.3" y2="25.4" width="0.1524" layer="94"/>
<wire x1="114.3" y1="25.4" x2="109.22" y2="25.4" width="0.1524" layer="94"/>
<text x="10.16" y="10.16" size="1.778" layer="94">MiniCIM
DC Motor</text>
<text x="38.1" y="10.16" size="1.778" layer="94">MiniCIM
DC Motor</text>
<text x="30.48" y="7.62" size="1.778" layer="94" rot="R90">US Digital
Optical Encoder</text>
<text x="58.42" y="7.62" size="1.778" layer="94" rot="R90">US Digital
Optical Encoder</text>
<text x="86.36" y="7.62" size="1.778" layer="94" rot="R90">US Digital
Optical Encoder</text>
<text x="114.3" y="7.62" size="1.778" layer="94" rot="R90">US Digital
Optical Encoder</text>
<text x="66.04" y="10.16" size="1.778" layer="94">DC Motor
210-1101</text>
<text x="93.98" y="10.16" size="1.778" layer="94">DC Motor
210-1101</text>
<text x="121.92" y="10.16" size="1.778" layer="94">DC Motor
210-1101</text>
<text x="421.64" y="25.4" size="2.54" layer="91">Team Cephal
Power System</text>
</plain>
<instances>
<instance part="FRAME1" gate="G$1" x="0" y="0"/>
<instance part="FRAME1" gate="G$2" x="147.32" y="0"/>
<instance part="BAT1" gate="G$1" x="299.72" y="111.76" rot="R270"/>
<instance part="BAT2" gate="G$1" x="314.96" y="111.76" rot="R270"/>
<instance part="F1" gate="G$1" x="330.2" y="119.38"/>
<instance part="F2" gate="G$1" x="365.76" y="106.68" rot="R90"/>
<instance part="F3" gate="G$1" x="375.92" y="106.68" rot="R90"/>
<instance part="F4" gate="G$1" x="386.08" y="106.68" rot="R90"/>
<instance part="F5" gate="G$1" x="396.24" y="106.68" rot="R90"/>
<instance part="F6" gate="G$1" x="429.26" y="106.68" rot="R90"/>
<instance part="F7" gate="G$1" x="439.42" y="106.68" rot="R90"/>
<instance part="F8" gate="G$1" x="449.58" y="106.68" rot="R90"/>
<instance part="F9" gate="G$1" x="459.74" y="106.68" rot="R90"/>
<instance part="F10" gate="G$1" x="424.18" y="114.3"/>
<instance part="K1" gate="1" x="411.48" y="101.6" rot="R90"/>
<instance part="K1" gate="2" x="414.02" y="114.3" rot="R90"/>
<instance part="S1" gate="G$1" x="345.44" y="119.38" rot="R270"/>
<instance part="CHG" gate="-2" x="312.42" y="78.74" rot="MR0"/>
<instance part="CHG" gate="-1" x="312.42" y="81.28" rot="MR0"/>
<instance part="F11" gate="G$1" x="370.84" y="119.38"/>
<instance part="FRAME2" gate="G$1" x="271.78" y="0"/>
<instance part="FRAME2" gate="G$2" x="419.1" y="0"/>
</instances>
<busses>
</busses>
<nets>
<net name="12V" class="0">
<segment>
<pinref part="BAT1" gate="G$1" pin="+"/>
<wire x1="299.72" y1="116.84" x2="299.72" y2="119.38" width="0.1524" layer="91"/>
<pinref part="F1" gate="G$1" pin="1"/>
<wire x1="299.72" y1="119.38" x2="314.96" y2="119.38" width="0.1524" layer="91"/>
<pinref part="BAT2" gate="G$1" pin="+"/>
<wire x1="314.96" y1="119.38" x2="322.58" y2="119.38" width="0.1524" layer="91"/>
<wire x1="314.96" y1="116.84" x2="314.96" y2="119.38" width="0.1524" layer="91"/>
<junction x="314.96" y="119.38"/>
<label x="304.8" y="119.38" size="1.778" layer="95"/>
</segment>
</net>
<net name="N$2" class="0">
<segment>
<pinref part="BAT1" gate="G$1" pin="-"/>
<wire x1="299.72" y1="106.68" x2="299.72" y2="101.6" width="0.1524" layer="91"/>
<wire x1="299.72" y1="101.6" x2="314.96" y2="101.6" width="0.1524" layer="91"/>
<pinref part="BAT2" gate="G$1" pin="-"/>
<wire x1="314.96" y1="101.6" x2="314.96" y2="106.68" width="0.1524" layer="91"/>
<wire x1="314.96" y1="101.6" x2="325.12" y2="101.6" width="0.1524" layer="91"/>
<wire x1="325.12" y1="101.6" x2="325.12" y2="78.74" width="0.1524" layer="91"/>
<wire x1="325.12" y1="78.74" x2="365.76" y2="78.74" width="0.1524" layer="91"/>
<pinref part="CHG" gate="-2" pin="S"/>
<wire x1="365.76" y1="78.74" x2="375.92" y2="78.74" width="0.1524" layer="91"/>
<wire x1="375.92" y1="78.74" x2="386.08" y2="78.74" width="0.1524" layer="91"/>
<wire x1="386.08" y1="78.74" x2="396.24" y2="78.74" width="0.1524" layer="91"/>
<wire x1="396.24" y1="78.74" x2="416.56" y2="78.74" width="0.1524" layer="91"/>
<wire x1="416.56" y1="78.74" x2="439.42" y2="78.74" width="0.1524" layer="91"/>
<wire x1="439.42" y1="78.74" x2="449.58" y2="78.74" width="0.1524" layer="91"/>
<wire x1="449.58" y1="78.74" x2="459.74" y2="78.74" width="0.1524" layer="91"/>
<wire x1="314.96" y1="78.74" x2="325.12" y2="78.74" width="0.1524" layer="91"/>
<junction x="325.12" y="78.74"/>
<junction x="314.96" y="101.6"/>
<wire x1="365.76" y1="78.74" x2="365.76" y2="83.82" width="0.1524" layer="91"/>
<wire x1="375.92" y1="78.74" x2="375.92" y2="83.82" width="0.1524" layer="91"/>
<wire x1="386.08" y1="78.74" x2="386.08" y2="83.82" width="0.1524" layer="91"/>
<wire x1="396.24" y1="78.74" x2="396.24" y2="83.82" width="0.1524" layer="91"/>
<wire x1="439.42" y1="78.74" x2="439.42" y2="83.82" width="0.1524" layer="91"/>
<wire x1="449.58" y1="78.74" x2="449.58" y2="83.82" width="0.1524" layer="91"/>
<wire x1="459.74" y1="78.74" x2="459.74" y2="83.82" width="0.1524" layer="91"/>
<junction x="365.76" y="78.74"/>
<junction x="375.92" y="78.74"/>
<junction x="386.08" y="78.74"/>
<junction x="396.24" y="78.74"/>
<junction x="449.58" y="78.74"/>
<junction x="459.74" y="78.74"/>
<junction x="439.42" y="78.74"/>
<pinref part="K1" gate="1" pin="2"/>
<wire x1="416.56" y1="101.6" x2="416.56" y2="78.74" width="0.1524" layer="91"/>
</segment>
</net>
<net name="N$4" class="0">
<segment>
<wire x1="350.52" y1="119.38" x2="360.68" y2="119.38" width="0.1524" layer="91"/>
<pinref part="F11" gate="G$1" pin="1"/>
<wire x1="360.68" y1="119.38" x2="363.22" y2="119.38" width="0.1524" layer="91"/>
<wire x1="360.68" y1="119.38" x2="360.68" y2="127" width="0.1524" layer="91"/>
<wire x1="360.68" y1="127" x2="403.86" y2="127" width="0.1524" layer="91"/>
<wire x1="403.86" y1="127" x2="403.86" y2="119.38" width="0.1524" layer="91"/>
<wire x1="403.86" y1="119.38" x2="408.94" y2="119.38" width="0.1524" layer="91"/>
<junction x="360.68" y="119.38"/>
<pinref part="K1" gate="2" pin="O"/>
</segment>
</net>
<net name="PC_PWR" class="0">
<segment>
<pinref part="F11" gate="G$1" pin="2"/>
<wire x1="375.92" y1="119.38" x2="375.92" y2="114.3" width="0.1524" layer="91"/>
<wire x1="375.92" y1="114.3" x2="365.76" y2="114.3" width="0.1524" layer="91"/>
<wire x1="365.76" y1="114.3" x2="365.76" y2="111.76" width="0.1524" layer="91"/>
<wire x1="375.92" y1="114.3" x2="375.92" y2="111.76" width="0.1524" layer="91"/>
<wire x1="375.92" y1="114.3" x2="386.08" y2="114.3" width="0.1524" layer="91"/>
<wire x1="386.08" y1="114.3" x2="386.08" y2="111.76" width="0.1524" layer="91"/>
<wire x1="386.08" y1="114.3" x2="396.24" y2="114.3" width="0.1524" layer="91"/>
<wire x1="396.24" y1="114.3" x2="396.24" y2="111.76" width="0.1524" layer="91"/>
<junction x="375.92" y="114.3"/>
<pinref part="F2" gate="G$1" pin="2"/>
<pinref part="F3" gate="G$1" pin="2"/>
<pinref part="F4" gate="G$1" pin="2"/>
<pinref part="F5" gate="G$1" pin="2"/>
<label x="381" y="114.3" size="1.778" layer="95"/>
</segment>
</net>
<net name="N$6" class="0">
<segment>
<pinref part="F1" gate="G$1" pin="2"/>
<wire x1="335.28" y1="119.38" x2="337.82" y2="119.38" width="0.1524" layer="91"/>
<pinref part="CHG" gate="-1" pin="S"/>
<wire x1="337.82" y1="119.38" x2="340.36" y2="119.38" width="0.1524" layer="91"/>
<wire x1="314.96" y1="81.28" x2="337.82" y2="81.28" width="0.1524" layer="91"/>
<wire x1="337.82" y1="81.28" x2="337.82" y2="119.38" width="0.1524" layer="91"/>
<junction x="337.82" y="119.38"/>
</segment>
</net>
<net name="MOT_PWR" class="0">
<segment>
<pinref part="F10" gate="G$1" pin="2"/>
<wire x1="429.26" y1="114.3" x2="439.42" y2="114.3" width="0.1524" layer="91"/>
<wire x1="429.26" y1="114.3" x2="429.26" y2="111.76" width="0.1524" layer="91"/>
<wire x1="439.42" y1="114.3" x2="439.42" y2="111.76" width="0.1524" layer="91"/>
<wire x1="439.42" y1="114.3" x2="449.58" y2="114.3" width="0.1524" layer="91"/>
<wire x1="449.58" y1="114.3" x2="449.58" y2="111.76" width="0.1524" layer="91"/>
<wire x1="449.58" y1="114.3" x2="459.74" y2="114.3" width="0.1524" layer="91"/>
<wire x1="459.74" y1="114.3" x2="459.74" y2="111.76" width="0.1524" layer="91"/>
<pinref part="F6" gate="G$1" pin="2"/>
<pinref part="F7" gate="G$1" pin="2"/>
<pinref part="F8" gate="G$1" pin="2"/>
<pinref part="F9" gate="G$1" pin="2"/>
<label x="434.34" y="114.3" size="1.778" layer="95"/>
</segment>
</net>
<net name="N$7" class="0">
<segment>
<pinref part="K1" gate="2" pin="P"/>
<pinref part="F10" gate="G$1" pin="1"/>
</segment>
</net>
<net name="WL_ENABLE" class="0">
<segment>
<pinref part="K1" gate="1" pin="1"/>
<wire x1="406.4" y1="101.6" x2="406.4" y2="91.44" width="0.1524" layer="91"/>
<wire x1="406.4" y1="91.44" x2="398.78" y2="91.44" width="0.1524" layer="91"/>
<label x="401.32" y="88.9" size="1.778" layer="95"/>
</segment>
</net>
<net name="FLASH/!SOLID" class="0">
<segment>
<pinref part="F6" gate="G$1" pin="1"/>
<wire x1="429.26" y1="99.06" x2="429.26" y2="71.12" width="0.1524" layer="91"/>
<label x="429.26" y="81.28" size="1.778" layer="95" rot="R90"/>
<wire x1="388.62" y1="91.44" x2="391.16" y2="91.44" width="0.1524" layer="91"/>
<wire x1="391.16" y1="91.44" x2="391.16" y2="71.12" width="0.1524" layer="91"/>
<wire x1="391.16" y1="71.12" x2="429.26" y2="71.12" width="0.1524" layer="91"/>
</segment>
</net>
<net name="GIGE" class="0">
<segment>
<wire x1="50.8" y1="170.18" x2="88.9" y2="170.18" width="0.1524" layer="91"/>
<label x="55.88" y="167.64" size="1.778" layer="95"/>
</segment>
</net>
<net name="USB" class="0">
<segment>
<wire x1="50.8" y1="124.46" x2="88.9" y2="124.46" width="0.1524" layer="91"/>
<label x="55.88" y="121.92" size="1.778" layer="95"/>
</segment>
<segment>
<wire x1="27.94" y1="119.38" x2="27.94" y2="88.9" width="0.1524" layer="91"/>
<label x="30.48" y="99.06" size="1.778" layer="95" rot="R90"/>
</segment>
<segment>
<wire x1="35.56" y1="119.38" x2="35.56" y2="104.14" width="0.1524" layer="91"/>
<wire x1="35.56" y1="104.14" x2="55.88" y2="104.14" width="0.1524" layer="91"/>
<wire x1="55.88" y1="104.14" x2="55.88" y2="88.9" width="0.1524" layer="91"/>
<label x="43.18" y="101.6" size="1.778" layer="95"/>
</segment>
<segment>
<wire x1="43.18" y1="119.38" x2="43.18" y2="109.22" width="0.1524" layer="91"/>
<wire x1="43.18" y1="109.22" x2="83.82" y2="109.22" width="0.1524" layer="91"/>
<wire x1="83.82" y1="109.22" x2="83.82" y2="88.9" width="0.1524" layer="91"/>
<label x="55.88" y="106.68" size="1.778" layer="95"/>
</segment>
</net>
<net name="+5V" class="0">
<segment>
<wire x1="116.84" y1="124.46" x2="137.16" y2="124.46" width="0.1524" layer="91"/>
<label x="119.38" y="124.46" size="1.778" layer="95"/>
</segment>
</net>
<net name="SCL" class="0">
<segment>
<wire x1="116.84" y1="121.92" x2="137.16" y2="121.92" width="0.1524" layer="91"/>
<label x="119.38" y="121.92" size="1.778" layer="95"/>
</segment>
</net>
<net name="SDA" class="0">
<segment>
<wire x1="116.84" y1="119.38" x2="137.16" y2="119.38" width="0.1524" layer="91"/>
<label x="119.38" y="119.38" size="1.778" layer="95"/>
</segment>
</net>
<net name="COM" class="0">
<segment>
<wire x1="116.84" y1="116.84" x2="137.16" y2="116.84" width="0.1524" layer="91"/>
<label x="119.38" y="116.84" size="1.778" layer="95"/>
</segment>
</net>
<net name="GIGE/POE" class="0">
<segment>
<wire x1="124.46" y1="165.1" x2="127" y2="165.1" width="0.1524" layer="91"/>
<wire x1="127" y1="165.1" x2="127" y2="162.56" width="0.1524" layer="91"/>
<wire x1="127" y1="162.56" x2="144.78" y2="162.56" width="0.1524" layer="91"/>
<label x="129.54" y="160.02" size="1.778" layer="95"/>
</segment>
<segment>
<wire x1="114.3" y1="165.1" x2="114.3" y2="152.4" width="0.1524" layer="91"/>
<wire x1="114.3" y1="152.4" x2="116.84" y2="149.86" width="0.1524" layer="91"/>
<wire x1="116.84" y1="149.86" x2="144.78" y2="149.86" width="0.1524" layer="91"/>
<label x="129.54" y="147.32" size="1.778" layer="95"/>
</segment>
<segment>
<wire x1="99.06" y1="165.1" x2="99.06" y2="142.24" width="0.1524" layer="91"/>
<wire x1="99.06" y1="142.24" x2="104.14" y2="137.16" width="0.1524" layer="91"/>
<wire x1="104.14" y1="137.16" x2="144.78" y2="137.16" width="0.1524" layer="91"/>
<label x="129.54" y="134.62" size="1.778" layer="95"/>
</segment>
</net>
<net name="M1+" class="0">
<segment>
<wire x1="10.16" y1="17.78" x2="10.16" y2="35.56" width="0.1524" layer="91"/>
<wire x1="10.16" y1="35.56" x2="20.32" y2="35.56" width="0.1524" layer="91"/>
<wire x1="20.32" y1="35.56" x2="20.32" y2="66.04" width="0.1524" layer="91"/>
<label x="10.16" y="25.4" size="1.778" layer="95" rot="R90"/>
</segment>
</net>
<net name="M1-" class="0">
<segment>
<wire x1="20.32" y1="17.78" x2="20.32" y2="33.02" width="0.1524" layer="91"/>
<wire x1="20.32" y1="33.02" x2="22.86" y2="33.02" width="0.1524" layer="91"/>
<wire x1="22.86" y1="33.02" x2="22.86" y2="66.04" width="0.1524" layer="91"/>
<label x="20.32" y="25.4" size="1.778" layer="95" rot="R90"/>
</segment>
</net>
<net name="M2+" class="0">
<segment>
<wire x1="38.1" y1="17.78" x2="38.1" y2="30.48" width="0.1524" layer="91"/>
<wire x1="38.1" y1="30.48" x2="30.48" y2="30.48" width="0.1524" layer="91"/>
<wire x1="30.48" y1="30.48" x2="30.48" y2="66.04" width="0.1524" layer="91"/>
<label x="38.1" y="25.4" size="1.778" layer="95" rot="R90"/>
</segment>
</net>
<net name="M2-" class="0">
<segment>
<wire x1="33.02" y1="66.04" x2="33.02" y2="33.02" width="0.1524" layer="91"/>
<wire x1="33.02" y1="33.02" x2="48.26" y2="33.02" width="0.1524" layer="91"/>
<wire x1="48.26" y1="33.02" x2="48.26" y2="17.78" width="0.1524" layer="91"/>
<label x="48.26" y="25.4" size="1.778" layer="95" rot="R90"/>
</segment>
</net>
<net name="M3+" class="0">
<segment>
<wire x1="66.04" y1="17.78" x2="66.04" y2="38.1" width="0.1524" layer="91"/>
<wire x1="66.04" y1="38.1" x2="48.26" y2="38.1" width="0.1524" layer="91"/>
<wire x1="48.26" y1="38.1" x2="48.26" y2="66.04" width="0.1524" layer="91"/>
<label x="66.04" y="25.4" size="1.778" layer="95" rot="R90"/>
</segment>
</net>
<net name="M3-" class="0">
<segment>
<wire x1="76.2" y1="17.78" x2="76.2" y2="40.64" width="0.1524" layer="91"/>
<wire x1="76.2" y1="40.64" x2="50.8" y2="40.64" width="0.1524" layer="91"/>
<wire x1="50.8" y1="40.64" x2="50.8" y2="66.04" width="0.1524" layer="91"/>
<label x="76.2" y="25.4" size="1.778" layer="95" rot="R90"/>
</segment>
</net>
<net name="M4+" class="0">
<segment>
<wire x1="93.98" y1="17.78" x2="93.98" y2="48.26" width="0.1524" layer="91"/>
<wire x1="93.98" y1="48.26" x2="58.42" y2="48.26" width="0.1524" layer="91"/>
<wire x1="58.42" y1="48.26" x2="58.42" y2="66.04" width="0.1524" layer="91"/>
<label x="93.98" y="25.4" size="1.778" layer="95" rot="R90"/>
</segment>
</net>
<net name="M4-" class="0">
<segment>
<wire x1="60.96" y1="66.04" x2="60.96" y2="50.8" width="0.1524" layer="91"/>
<wire x1="60.96" y1="50.8" x2="104.14" y2="50.8" width="0.1524" layer="91"/>
<wire x1="104.14" y1="50.8" x2="104.14" y2="17.78" width="0.1524" layer="91"/>
<label x="104.14" y="25.4" size="1.778" layer="95" rot="R90"/>
</segment>
</net>
<net name="M5+" class="0">
<segment>
<wire x1="121.92" y1="17.78" x2="121.92" y2="60.96" width="0.1524" layer="91"/>
<wire x1="121.92" y1="60.96" x2="78.74" y2="60.96" width="0.1524" layer="91"/>
<wire x1="78.74" y1="60.96" x2="78.74" y2="66.04" width="0.1524" layer="91"/>
<label x="121.92" y="25.4" size="1.778" layer="95" rot="R90"/>
</segment>
</net>
<net name="M5-" class="0">
<segment>
<wire x1="81.28" y1="66.04" x2="81.28" y2="63.5" width="0.1524" layer="91"/>
<wire x1="81.28" y1="63.5" x2="132.08" y2="63.5" width="0.1524" layer="91"/>
<wire x1="132.08" y1="63.5" x2="132.08" y2="17.78" width="0.1524" layer="91"/>
<label x="132.08" y="25.4" size="1.778" layer="95" rot="R90"/>
</segment>
</net>
<net name="QUADRATURE1" class="0">
<segment>
<wire x1="27.94" y1="25.4" x2="27.94" y2="27.94" width="0.1524" layer="91"/>
<wire x1="27.94" y1="27.94" x2="25.4" y2="27.94" width="0.1524" layer="91"/>
<wire x1="25.4" y1="27.94" x2="25.4" y2="66.04" width="0.1524" layer="91"/>
<label x="25.4" y="38.1" size="1.778" layer="95" rot="R90"/>
</segment>
</net>
<net name="QUADRATURE2" class="0">
<segment>
<wire x1="55.88" y1="25.4" x2="55.88" y2="35.56" width="0.1524" layer="91"/>
<wire x1="55.88" y1="35.56" x2="35.56" y2="35.56" width="0.1524" layer="91"/>
<wire x1="35.56" y1="35.56" x2="35.56" y2="66.04" width="0.1524" layer="91"/>
<label x="35.56" y="38.1" size="1.778" layer="95" rot="R90"/>
</segment>
</net>
<net name="QUADRATURE4" class="0">
<segment>
<wire x1="111.76" y1="25.4" x2="111.76" y2="53.34" width="0.1524" layer="91"/>
<wire x1="111.76" y1="53.34" x2="63.5" y2="53.34" width="0.1524" layer="91"/>
<wire x1="63.5" y1="53.34" x2="63.5" y2="66.04" width="0.1524" layer="91"/>
<label x="71.12" y="53.34" size="1.778" layer="95"/>
</segment>
</net>
<net name="QUADRATURE3" class="0">
<segment>
<wire x1="83.82" y1="25.4" x2="83.82" y2="43.18" width="0.1524" layer="91"/>
<wire x1="83.82" y1="43.18" x2="53.34" y2="43.18" width="0.1524" layer="91"/>
<wire x1="53.34" y1="43.18" x2="53.34" y2="66.04" width="0.1524" layer="91"/>
<label x="58.42" y="43.18" size="1.778" layer="95"/>
</segment>
</net>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
<compatibility>
<note version="6.3" minversion="6.2.2" severity="warning">
Since Version 6.2.2 text objects can contain more than one line,
which will not be processed correctly with this version.
</note>
</compatibility>
</eagle>
