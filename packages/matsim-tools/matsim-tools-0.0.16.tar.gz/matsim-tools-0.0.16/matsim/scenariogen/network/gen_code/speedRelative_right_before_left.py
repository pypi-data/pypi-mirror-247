# -*- coding: utf-8 -*-
def features(ft, data):
		data[0] = (ft.get("length") - 90.22617266187049) / 60.92023402293393
		data[1] = (ft.get("speed") - 8.338) / 0.21075103795711186
		data[2] = (ft.get("num_foes") - 6.054676258992806) / 2.530368728542543
		data[3] = (ft.get("num_lanes") - 1.0) / 1.0
		data[4] = (ft.get("junction_inc_lanes") - 3.181294964028777) / 0.47249046967264163
		data[5] = ft.get("change_speed")
		data[6] = ft.get("dir_l")
		data[7] = ft.get("dir_r")
		data[8] = ft.get("dir_s")
		data[9] = ft.get("dir_multiple_s")
		data[10] = ft.get("dir_exclusive")
		data[11] = ft.get("priority_lower")
		data[12] = ft.get("priority_equal")
		data[13] = ft.get("priority_higher")
		data[14] = ft.get("num_to_links")
		data[15] = ft.get("change_num_lanes")
		data[16] = ft.get("is_secondary_or_higher")
		data[17] = ft.get("is_primary_or_higher")
		data[18] = ft.get("is_motorway")
		data[19] = ft.get("is_link")

params = [0.9305278304345926, 0.9043229043683589, 0.8985526110903621, 0.9191080983457031, 0.8907142857142857, 0.940893110206543, 0.884, 0.9613095238095237, 0.9228423007791429, 0.8300000000000001, 0.8943438766603578, 0.8769191919191919, 0.9264409508645753, 0.9484851130107215, 0.9340312849353027, 0.9124578901257473, 0.8582051282051282, 0.909797759034444, 0.9344293563579279, 0.9226230642742272, 0.951236987818383, 0.917750933706816, 0.858125, 0.8967592592592594, 0.9086388395636742, 0.9229635143482734, 0.9413541666666668, 0.9222546377233879, 0.9531507936507936, 0.884, 0.9232737170765741, 0.9420366908884765, 0.8543589743589742, 0.9058668134916806, 0.8738095238095238, 0.9366928945237768, 0.86, 0.9207508674231751, 0.902090368605191, 0.8525, 0.9387968584122431, 0.9705454545454547, 0.9141657905747677, 0.9335666107613368, 0.8948620046620046, 0.9352028347028346, 0.8962287664795469, 0.9126794765405561, 0.9374504827323975, 0.86, 0.8985344537815128, 0.98, 0.9234912715260929, 0.901185165083988, 0.8672172619047619, 0.8771428571428571, 0.9380861378764609, 0.9238785164707894, 0.9038379914529914, 0.9308401447673033, 0.9036971596960651, 0.9195601851851853, 0.8907142857142857, 0.9449098639455782, 0.9331651882924081, 0.8937773115773116, 0.9119973042830187, 0.8885302763080541, 0.83, 0.9346947265205245, 0.9133718589362877, 0.937355790859467, 0.8887647058823529, 0.8300000000000001, 0.9186991165034641, 0.8970945022948749, 0.8804879968516333, 0.9225565663726105, 0.9377266325085472, 0.8951074099511598, 0.9413564497300451, 0.8849072456094779, 0.9046265735601252, 0.8837777777777778, 0.9303421225116348, 0.9277892156862745, 0.9638080357142857, 0.9221160733206191, 0.9445047225501771, 0.8547619047619047, 0.9026749569833273, 0.9355929043062932, 0.8971044417767108, 0.86, 0.9075397546897547, 0.9309147201178452, 0.8998934923670057, 0.9221474519632414, 0.9345637509256911, 0.949569130216189, 0.86, 0.98, 0.9214163729704636, 0.8639583333333333, 0.9078645868020868, 0.84, 0.9252300192648132, 0.9377153337399736, 0.8929320309320309, 0.9321039755074404, 0.9037339153505353, 0.9217383498854088, 0.9336417130112384, 0.9115921985815603, 0.9503561539035675, 0.8935294117647059, 0.9270503017111714, 0.8522222222222222, 0.96, 0.8868765902687469, 0.9479472302388969, 0.9335912807562808, 0.9060185223208942, 0.9299265911751908, 0.8956062610229277, 0.9295456775456773, 0.9033918642408219, 0.9238201058201057, 0.905, 0.9398998078132692, 0.9082240896358543, 0.9023313797313797, 0.9359469193219193, 0.9067863772258606, 0.8588888888888889, 0.9291570194691746, 0.9518617724867722, 0.8841058823529412, 0.9321543507774276, 0.9127678571428571, 0.9030415850854671, 0.923777452511059, 0.9369167386012045, 0.9491933871587849, 0.86, 0.9063899529042386, 0.932301291523647, 0.8743939393939395, 0.9100911547428562, 0.9283333333333333, 0.9591666666666667, 0.8682142857142857, 0.9325253360629007, 0.9209195481042254, 0.947332336523126, 0.8856660387634963, 0.9020793679922561, 0.9382138501742161, 0.9264073119617818, 0.9534775641025638, 0.9177784002489885, 0.9124728676341581, 0.9362699437051292, 0.9087866330789074, 0.8616666666666667, 0.9429917800453514, 0.963125, 0.84, 0.9332464645151662, 0.9336905432275509, 0.9113936507936508, 0.9006994513923483, 0.9248823996265172, 0.8738095238095238, 0.9298310151111443, 0.9396822787848432, 0.8984040479987849, 0.9333993081128117, 0.825, 0.9111644099710055, 0.9400266290726816, 0.9102272727272727, 0.84, 0.9446908480980647, 0.9368222222222222, 0.8731746031746032, 0.8952777777777777, 0.9421804004595103, 0.881712962962963, 0.9113632939482633, 0.86, 0.9362446946435916, 0.9040221947364804, 0.9315219315854395, 0.8615432098765433, 0.9094983595636535, 0.8738095238095238, 0.86, 0.9384398451789752, 0.8943360079074365, 0.9385057563648473, 0.893085162832337, 0.91455450967502, 0.9366619478712507, 0.91, 0.9642476190476191, 0.9457244047619046, 0.8869013278388279, 0.9335353084415584, 0.8959724997224997, 0.9131430444299826, 0.8738095238095238, 0.86, 0.9398375871153526, 0.8533333333333334, 0.9023309659181148, 0.917110310307508, 0.9319668368911791, 0.9529848484848483, 0.9040661764705883]
def score(params, inputs):
    if inputs[0] <= 0.37251707911491394:
        if inputs[7] <= 0.5:
            if inputs[0] <= -0.019388840068131685:
                var0 = params[0]
            else:
                var0 = params[1]
        else:
            if inputs[0] <= -0.5582902729511261:
                var0 = params[2]
            else:
                var0 = params[3]
    else:
        if inputs[0] <= 4.441608428955078:
            if inputs[2] <= -1.0096063315868378:
                var0 = params[4]
            else:
                var0 = params[5]
        else:
            var0 = params[6]
    if inputs[0] <= -0.6265762746334076:
        if inputs[7] <= 0.5:
            if inputs[0] <= -1.1603890657424927:
                var1 = params[7]
            else:
                var1 = params[8]
        else:
            if inputs[12] <= 0.5:
                var1 = params[9]
            else:
                var1 = params[10]
    else:
        if inputs[10] <= 0.5:
            var1 = params[11]
        else:
            if inputs[0] <= 1.3471522331237793:
                var1 = params[12]
            else:
                var1 = params[13]
    if inputs[0] <= 0.37251707911491394:
        if inputs[7] <= 0.5:
            if inputs[0] <= -0.24246742576360703:
                var2 = params[14]
            else:
                var2 = params[15]
        else:
            if inputs[2] <= -0.6144070029258728:
                var2 = params[16]
            else:
                var2 = params[17]
    else:
        if inputs[0] <= 1.3500248193740845:
            if inputs[0] <= 0.7356148362159729:
                var2 = params[18]
            else:
                var2 = params[19]
        else:
            if inputs[0] <= 3.6622287034988403:
                var2 = params[20]
            else:
                var2 = params[21]
    if inputs[0] <= 0.37251707911491394:
        if inputs[10] <= 0.5:
            if inputs[0] <= 0.21682167798280716:
                var3 = params[22]
            else:
                var3 = params[23]
        else:
            if inputs[0] <= -0.5582902729511261:
                var3 = params[24]
            else:
                var3 = params[25]
    else:
        if inputs[0] <= 1.425533413887024:
            if inputs[0] <= 0.7100896239280701:
                var3 = params[26]
            else:
                var3 = params[27]
        else:
            if inputs[0] <= 4.274340510368347:
                var3 = params[28]
            else:
                var3 = params[29]
    if inputs[0] <= 0.18530505895614624:
        if inputs[7] <= 0.5:
            if inputs[0] <= -0.604580283164978:
                var4 = params[30]
            else:
                var4 = params[31]
        else:
            if inputs[10] <= 0.5:
                var4 = params[32]
            else:
                var4 = params[33]
    else:
        if inputs[2] <= -1.0096063315868378:
            var4 = params[34]
        else:
            if inputs[1] <= 13.152960108593106:
                var4 = params[35]
            else:
                var4 = params[36]
    if inputs[0] <= -0.6042519807815552:
        if inputs[0] <= -0.6124594509601593:
            if inputs[7] <= 0.5:
                var5 = params[37]
            else:
                var5 = params[38]
        else:
            var5 = params[39]
    else:
        if inputs[7] <= 0.5:
            if inputs[0] <= 1.3526511788368225:
                var5 = params[40]
            else:
                var5 = params[41]
        else:
            if inputs[0] <= -0.012987025547772646:
                var5 = params[42]
            else:
                var5 = params[43]
    if inputs[0] <= 0.3813811242580414:
        if inputs[7] <= 0.5:
            if inputs[4] <= -1.4419232308864594:
                var6 = params[44]
            else:
                var6 = params[45]
        else:
            if inputs[0] <= -0.7939262390136719:
                var6 = params[46]
            else:
                var6 = params[47]
    else:
        if inputs[0] <= 3.9883108139038086:
            if inputs[1] <= 13.152960108593106:
                var6 = params[48]
            else:
                var6 = params[49]
        else:
            var6 = params[50]
    if inputs[0] <= -0.6249347925186157:
        if inputs[7] <= 0.5:
            if inputs[0] <= -1.2314655780792236:
                var7 = params[51]
            else:
                var7 = params[52]
        else:
            if inputs[0] <= -0.6603088974952698:
                var7 = params[53]
            else:
                var7 = params[54]
    else:
        if inputs[2] <= -0.6144070029258728:
            var7 = params[55]
        else:
            if inputs[7] <= 0.5:
                var7 = params[56]
            else:
                var7 = params[57]
    if inputs[0] <= 0.3396051824092865:
        if inputs[7] <= 0.5:
            if inputs[2] <= -0.6144070029258728:
                var8 = params[58]
            else:
                var8 = params[59]
        else:
            if inputs[0] <= -0.21759884804487228:
                var8 = params[60]
            else:
                var8 = params[61]
    else:
        if inputs[2] <= -1.0096063315868378:
            var8 = params[62]
        else:
            if inputs[8] <= 0.5:
                var8 = params[63]
            else:
                var8 = params[64]
    if inputs[0] <= -0.649064689874649:
        if inputs[0] <= -0.7174327671527863:
            if inputs[0] <= -1.0264434218406677:
                var9 = params[65]
            else:
                var9 = params[66]
        else:
            if inputs[0] <= -0.6557127237319946:
                var9 = params[67]
            else:
                var9 = params[68]
    else:
        if inputs[0] <= 0.3752255290746689:
            if inputs[7] <= 0.5:
                var9 = params[69]
            else:
                var9 = params[70]
        else:
            if inputs[0] <= 3.9883108139038086:
                var9 = params[71]
            else:
                var9 = params[72]
    if inputs[0] <= -0.6265762746334076:
        if inputs[0] <= -1.2984384298324585:
            var10 = params[73]
        else:
            if inputs[7] <= 0.5:
                var10 = params[74]
            else:
                var10 = params[75]
    else:
        if inputs[4] <= -1.4419232308864594:
            var10 = params[76]
        else:
            if inputs[0] <= 0.37251707911491394:
                var10 = params[77]
            else:
                var10 = params[78]
    if inputs[0] <= -0.2029075101017952:
        if inputs[7] <= 0.5:
            if inputs[2] <= -1.0096063315868378:
                var11 = params[79]
            else:
                var11 = params[80]
        else:
            if inputs[0] <= -0.7775934338569641:
                var11 = params[81]
            else:
                var11 = params[82]
    else:
        if inputs[0] <= 1.3471522331237793:
            if inputs[10] <= 0.5:
                var11 = params[83]
            else:
                var11 = params[84]
        else:
            if inputs[6] <= 0.5:
                var11 = params[85]
            else:
                var11 = params[86]
    if inputs[0] <= -0.12181786075234413:
        if inputs[7] <= 0.5:
            if inputs[0] <= -0.604580283164978:
                var12 = params[87]
            else:
                var12 = params[88]
        else:
            if inputs[0] <= -1.0750315189361572:
                var12 = params[89]
            else:
                var12 = params[90]
    else:
        if inputs[1] <= 13.152960108593106:
            if inputs[0] <= 3.9883108139038086:
                var12 = params[91]
            else:
                var12 = params[92]
        else:
            var12 = params[93]
    if inputs[0] <= 0.333449587225914:
        if inputs[7] <= 0.5:
            if inputs[2] <= -0.6144070029258728:
                var13 = params[94]
            else:
                var13 = params[95]
        else:
            if inputs[0] <= -0.24566834419965744:
                var13 = params[96]
            else:
                var13 = params[97]
    else:
        if inputs[1] <= 13.152960108593106:
            if inputs[0] <= 1.6379422545433044:
                var13 = params[98]
            else:
                var13 = params[99]
        else:
            var13 = params[100]
    if inputs[0] <= -0.12181786075234413:
        if inputs[7] <= 0.5:
            if inputs[0] <= -1.2314655780792236:
                var14 = params[101]
            else:
                var14 = params[102]
        else:
            if inputs[10] <= 0.5:
                var14 = params[103]
            else:
                var14 = params[104]
    else:
        if inputs[4] <= -1.4419232308864594:
            var14 = params[105]
        else:
            if inputs[0] <= 0.3588106334209442:
                var14 = params[106]
            else:
                var14 = params[107]
    if inputs[0] <= -0.14225442707538605:
        if inputs[7] <= 0.5:
            if inputs[2] <= -0.6144070029258728:
                var15 = params[108]
            else:
                var15 = params[109]
        else:
            if inputs[0] <= -0.3111638128757477:
                var15 = params[110]
            else:
                var15 = params[111]
    else:
        if inputs[0] <= 1.092721164226532:
            if inputs[2] <= -0.21920768730342388:
                var15 = params[112]
            else:
                var15 = params[113]
        else:
            if inputs[0] <= 3.9883108139038086:
                var15 = params[114]
            else:
                var15 = params[115]
    if inputs[0] <= -0.6515268981456757:
        if inputs[7] <= 0.5:
            if inputs[0] <= -0.689691573381424:
                var16 = params[116]
            else:
                var16 = params[117]
        else:
            if inputs[0] <= -1.2552672028541565:
                var16 = params[118]
            else:
                var16 = params[119]
    else:
        if inputs[7] <= 0.5:
            if inputs[0] <= -0.24246742576360703:
                var16 = params[120]
            else:
                var16 = params[121]
        else:
            if inputs[0] <= -0.23655806481838226:
                var16 = params[122]
            else:
                var16 = params[123]
    if inputs[0] <= 0.3396051824092865:
        if inputs[7] <= 0.5:
            if inputs[2] <= -0.6144070029258728:
                var17 = params[124]
            else:
                var17 = params[125]
        else:
            if inputs[0] <= -0.2189120426774025:
                var17 = params[126]
            else:
                var17 = params[127]
    else:
        if inputs[10] <= 0.5:
            var17 = params[128]
        else:
            if inputs[0] <= 3.9883108139038086:
                var17 = params[129]
            else:
                var17 = params[130]
    if inputs[0] <= -0.011755907908082008:
        if inputs[7] <= 0.5:
            if inputs[2] <= -0.6144070029258728:
                var18 = params[131]
            else:
                var18 = params[132]
        else:
            if inputs[0] <= -0.035967896692454815:
                var18 = params[133]
            else:
                var18 = params[134]
    else:
        if inputs[0] <= 3.6622287034988403:
            if inputs[0] <= 1.443261444568634:
                var18 = params[135]
            else:
                var18 = params[136]
        else:
            var18 = params[137]
    if inputs[0] <= 0.3752255290746689:
        if inputs[7] <= 0.5:
            if inputs[0] <= -0.24862302094697952:
                var19 = params[138]
            else:
                var19 = params[139]
        else:
            if inputs[0] <= -0.3435011953115463:
                var19 = params[140]
            else:
                var19 = params[141]
    else:
        if inputs[1] <= 13.152960108593106:
            if inputs[0] <= 1.3969714641571045:
                var19 = params[142]
            else:
                var19 = params[143]
        else:
            var19 = params[144]
    if inputs[0] <= 0.0021967634093016386:
        if inputs[7] <= 0.5:
            if inputs[2] <= -0.6144070029258728:
                var20 = params[145]
            else:
                var20 = params[146]
        else:
            if inputs[10] <= 0.5:
                var20 = params[147]
            else:
                var20 = params[148]
    else:
        if inputs[0] <= 0.14361119270324707:
            if inputs[8] <= 0.5:
                var20 = params[149]
            else:
                var20 = params[150]
        else:
            if inputs[0] <= 0.17061371356248856:
                var20 = params[151]
            else:
                var20 = params[152]
    if inputs[0] <= -0.24566834419965744:
        if inputs[7] <= 0.5:
            if inputs[0] <= -0.548359215259552:
                var21 = params[153]
            else:
                var21 = params[154]
        else:
            if inputs[0] <= -0.7491135597229004:
                var21 = params[155]
            else:
                var21 = params[156]
    else:
        if inputs[0] <= 1.3500248193740845:
            if inputs[0] <= -0.08923427015542984:
                var21 = params[157]
            else:
                var21 = params[158]
        else:
            if inputs[0] <= 3.6622287034988403:
                var21 = params[159]
            else:
                var21 = params[160]
    if inputs[0] <= 0.37251707911491394:
        if inputs[7] <= 0.5:
            if inputs[0] <= -0.7200591564178467:
                var22 = params[161]
            else:
                var22 = params[162]
        else:
            if inputs[14] <= 3.5:
                var22 = params[163]
            else:
                var22 = params[164]
    else:
        if inputs[0] <= 0.719199925661087:
            if inputs[0] <= 0.6613373756408691:
                var22 = params[165]
            else:
                var22 = params[166]
        else:
            if inputs[2] <= -1.0096063315868378:
                var22 = params[167]
            else:
                var22 = params[168]
    if inputs[0] <= 0.36578695476055145:
        if inputs[7] <= 0.5:
            if inputs[0] <= -0.24246742576360703:
                var23 = params[169]
            else:
                var23 = params[170]
        else:
            if inputs[0] <= -0.22851476073265076:
                var23 = params[171]
            else:
                var23 = params[172]
    else:
        if inputs[2] <= -1.0096063315868378:
            var23 = params[173]
        else:
            if inputs[6] <= 0.5:
                var23 = params[174]
            else:
                var23 = params[175]
    if inputs[0] <= 0.37251707911491394:
        if inputs[7] <= 0.5:
            if inputs[2] <= -0.6144070029258728:
                var24 = params[176]
            else:
                var24 = params[177]
        else:
            if inputs[2] <= -0.6144070029258728:
                var24 = params[178]
            else:
                var24 = params[179]
    else:
        if inputs[0] <= 0.6523091495037079:
            if inputs[0] <= 0.6051983833312988:
                var24 = params[180]
            else:
                var24 = params[181]
        else:
            if inputs[4] <= -1.4419232308864594:
                var24 = params[182]
            else:
                var24 = params[183]
    if inputs[7] <= 0.5:
        if inputs[2] <= -0.6144070029258728:
            if inputs[0] <= -0.7733255326747894:
                var25 = params[184]
            else:
                var25 = params[185]
        else:
            if inputs[0] <= -1.0219292640686035:
                var25 = params[186]
            else:
                var25 = params[187]
    else:
        if inputs[0] <= 0.3752255290746689:
            if inputs[10] <= 0.5:
                var25 = params[188]
            else:
                var25 = params[189]
        else:
            if inputs[5] <= -2.7799999713897705:
                var25 = params[190]
            else:
                var25 = params[191]
    if inputs[0] <= 0.37251707911491394:
        if inputs[7] <= 0.5:
            if inputs[2] <= -0.6144070029258728:
                var26 = params[192]
            else:
                var26 = params[193]
        else:
            if inputs[10] <= 0.5:
                var26 = params[194]
            else:
                var26 = params[195]
    else:
        if inputs[2] <= -1.0096063315868378:
            var26 = params[196]
        else:
            if inputs[5] <= -2.7799999713897705:
                var26 = params[197]
            else:
                var26 = params[198]
    if inputs[0] <= 0.33377788960933685:
        if inputs[7] <= 0.5:
            if inputs[2] <= -0.6144070029258728:
                var27 = params[199]
            else:
                var27 = params[200]
        else:
            if inputs[0] <= -0.6407751739025116:
                var27 = params[201]
            else:
                var27 = params[202]
    else:
        if inputs[0] <= 1.053899884223938:
            if inputs[0] <= 0.9791299998760223:
                var27 = params[203]
            else:
                var27 = params[204]
        else:
            if inputs[7] <= 0.5:
                var27 = params[205]
            else:
                var27 = params[206]
    if inputs[0] <= 0.37251707911491394:
        if inputs[7] <= 0.5:
            if inputs[2] <= -1.0096063315868378:
                var28 = params[207]
            else:
                var28 = params[208]
        else:
            if inputs[0] <= -0.6896094977855682:
                var28 = params[209]
            else:
                var28 = params[210]
    else:
        if inputs[2] <= -1.0096063315868378:
            var28 = params[211]
        else:
            if inputs[5] <= -2.7799999713897705:
                var28 = params[212]
            else:
                var28 = params[213]
    if inputs[0] <= 0.1900653839111328:
        if inputs[10] <= 0.5:
            var29 = params[214]
        else:
            if inputs[0] <= -0.6038416028022766:
                var29 = params[215]
            else:
                var29 = params[216]
    else:
        if inputs[0] <= 3.6622287034988403:
            if inputs[0] <= 1.4325917959213257:
                var29 = params[217]
            else:
                var29 = params[218]
        else:
            var29 = params[219]
    return (var0 + var1 + var2 + var3 + var4 + var5 + var6 + var7 + var8 + var9 + var10 + var11 + var12 + var13 + var14 + var15 + var16 + var17 + var18 + var19 + var20 + var21 + var22 + var23 + var24 + var25 + var26 + var27 + var28 + var29) * 0.03333333333333333

def batch_loss(params, inputs, targets):
    error = 0
    for x, y in zip(inputs, targets):
        preds = score(params, x)
        error += (preds - y) ** 2
    return error
