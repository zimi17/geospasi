<!DOCTYPE qgis PUBLIC 'http:/mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="Symbology" version="3.28">
  <renderer-v2 type="graduatedSymbol" graduatedMethod="GraduatedColor" attr="gap_persen" enableattributelegend="1" symbollevels="0">
    <ranges>
      <range symbol="0" render="true" lower="0.000000000000000" upper="25.000000000000000" label="0-25% (Rendah)"/>
      <range symbol="1" render="true" lower="25.000000000000000" upper="50.000000000000000" label="25-50% (Sedang)"/>
      <range symbol="2" render="true" lower="50.000000000000000" upper="75.000000000000000" label="50-75% (Tinggi)"/>
      <range symbol="3" render="true" lower="75.000000000000000" upper="100.000000000000000" label="75-100% (Kritis)"/>
    </ranges>
    <symbols>
      <symbol name="0" type="fill" alpha="0.8">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="color" v="68,191,64,255"/>
          <prop k="outline_color" v="255,255,255,255"/>
          <prop k="outline_width" v="0.5"/>
        </layer>
      </symbol>
      <symbol name="1" type="fill" alpha="0.8">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="color" v="255,217,71,255"/>
          <prop k="outline_color" v="255,255,255,255"/>
          <prop k="outline_width" v="0.5"/>
        </layer>
      </symbol>
      <symbol name="2" type="fill" alpha="0.8">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="color" v="255,128,0,255"/>
          <prop k="outline_color" v="255,255,255,255"/>
          <prop k="outline_width" v="0.5"/>
        </layer>
      </symbol>
      <symbol name="3" type="fill" alpha="0.8">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="color" v="214,37,37,255"/>
          <prop k="outline_color" v="255,255,255,255"/>
          <prop k="outline_width" v="0.5"/>
        </layer>
      </symbol>
    </symbols>
    <colorramp type="gradient" name="[source]">
      <prop k="color1" v="68,191,64,255"/>
      <prop k="color2" v="214,37,37,255"/>
    </colorramp>
    <classificationMethod id="EqualInterval">
      <symmetricMode astr="false" symmetrypoint="0" enabled="0"/>
      <labelFormat format="%1 - %2" labelprecision="0" trimtrailingzeroes="1"/>
    </classificationMethod>
  </renderer-v2>
</qgis>
