# -*- coding: utf-8 -*-
def features(ft, data):
		data[0] = (ft.get("length") - 86.86929539295392) / 80.82722944512284
		data[1] = (ft.get("speed") - 15.921680216802168) / 3.6421386992044624
		data[2] = (ft.get("num_foes") - 4.675338753387534) / 2.6912009502493186
		data[3] = (ft.get("num_lanes") - 1.9143631436314363) / 0.7371186034868321
		data[4] = (ft.get("junction_inc_lanes") - 5.772357723577236) / 1.9212674006705497
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

params = [311.20407, 421.60568, 223.16147, 308.2382, 316.2727, 400.71896, 234.13985, 339.72766, 246.46765, 317.30167, 144.7941, 201.15233, 167.6146, 220.72697, 128.56407, 172.50424, 200.97063, 257.48453, 312.14822, 259.27008, 179.73071, 91.67996, 270.433, 221.55682, 120.317696, 161.2052, 227.8468, 162.2525, 48.44423, 106.689865, 138.55296, 213.35568, 145.02211, 219.23206, 200.56686, 240.3822, 62.212936, 140.67691, 200.03795, 154.78278, 109.382355, 153.27013, 65.26072, 113.0085, 65.3399, 101.4157, 23.507172, 55.737885, 194.03343, 168.68817, 64.943184, 161.30928, 121.53563, 50.63623, 149.18245, 115.57299, 67.39543, 34.53273, 19.0587, 37.10447, 116.330574, 69.75224, 76.944626, 40.05574, 3.195991, 39.847504, 68.981285, 38.896763, 123.91969, 78.66716, 37.568516, 124.41242, 61.48837, 109.955986, 127.8411, 82.688934, 126.786026, 77.07099, 35.928726, 85.46076, -27.315186, 61.055424, 60.458485, 90.446785, 125.87344, 109.33868, 126.79179, 38.225384, -14.740204, 4.430801, 30.028364, 76.13142, 56.37024, 25.07083, 16.806404, 38.967163, 18.673769, 71.24041, 64.57933, 100.33942, 58.301178, -9.000764, -40.995327, 1.0057571, 54.55601, -22.749779, 48.145733, 73.898254, 56.74138, 19.649736, -26.678684, 17.676388, 46.32536, 11.516863, 46.94424, 115.144485, -19.079905, 38.217476, 63.849026, 31.490896, 6.594454, 74.92776, 52.95437, 110.08301, -15.959076, -11.833787, 18.264223, 0.19019526, 42.846096, 53.647465, 92.71424, 32.872772, -6.857015, -29.938574, 16.141563, 29.317196, -22.533772, 21.674593, -16.028393, 38.04493, 4.647673, 46.19219, -60.685505, -35.60854, 7.585011, -50.248325, 19.784641, 33.232395, -22.364368, 17.308252, -27.40714, 5.472665, -0.046366937, 95.12161, 19.808243, 41.392002]
def score(params, inputs):
    if inputs[15] >= -0.5:
        if inputs[9] >= 0.5:
            if inputs[0] >= -0.47371778:
                if inputs[14] >= 2.5:
                    var0 = params[0]
                else:
                    var0 = params[1]
            else:
                if inputs[1] >= 0.5857327:
                    var0 = params[2]
                else:
                    var0 = params[3]
        else:
            if inputs[0] >= -0.076141365:
                if inputs[6] >= 0.5:
                    var0 = params[4]
                else:
                    var0 = params[5]
            else:
                if inputs[4] >= -1.1827389:
                    var0 = params[6]
                else:
                    var0 = params[7]
    else:
        if inputs[9] >= 0.5:
            if inputs[15] >= -1.5:
                if inputs[4] >= -0.1417594:
                    var0 = params[8]
                else:
                    var0 = params[9]
            else:
                if inputs[14] >= 2.5:
                    var0 = params[10]
                else:
                    var0 = params[11]
        else:
            if inputs[0] >= -0.42293042:
                if inputs[7] >= 0.5:
                    var0 = params[12]
                else:
                    var0 = params[13]
            else:
                if inputs[4] >= -0.1417594:
                    var0 = params[14]
                else:
                    var0 = params[15]
    if inputs[15] >= -0.5:
        if inputs[0] >= -0.47408894:
            if inputs[7] >= 0.5:
                if inputs[4] >= -0.1417594:
                    var1 = params[16]
                else:
                    var1 = params[17]
            else:
                if inputs[0] >= -0.27310467:
                    var1 = params[18]
                else:
                    var1 = params[19]
        else:
            if inputs[0] >= -0.70321965:
                if inputs[0] >= -0.5652092:
                    var1 = params[20]
                else:
                    var1 = params[21]
            else:
                if inputs[8] >= 0.5:
                    var1 = params[22]
                else:
                    var1 = params[23]
    else:
        if inputs[0] >= -0.46153128:
            if inputs[7] >= 0.5:
                if inputs[10] >= 0.5:
                    var1 = params[24]
                else:
                    var1 = params[25]
            else:
                if inputs[9] >= 0.5:
                    var1 = params[26]
                else:
                    var1 = params[27]
        else:
            if inputs[0] >= -0.70241547:
                if inputs[1] >= -0.17618227:
                    var1 = params[28]
                else:
                    var1 = params[29]
            else:
                if inputs[10] >= 0.5:
                    var1 = params[30]
                else:
                    var1 = params[31]
    if inputs[15] >= -0.5:
        if inputs[0] >= -0.4083314:
            if inputs[7] >= 0.5:
                if inputs[6] >= 0.5:
                    var2 = params[32]
                else:
                    var2 = params[33]
            else:
                if inputs[4] >= -0.1417594:
                    var2 = params[34]
                else:
                    var2 = params[35]
        else:
            if inputs[0] >= -0.70321965:
                if inputs[1] >= -0.17618227:
                    var2 = params[36]
                else:
                    var2 = params[37]
            else:
                if inputs[8] >= 0.5:
                    var2 = params[38]
                else:
                    var2 = params[39]
    else:
        if inputs[15] >= -1.5:
            if inputs[0] >= -0.46728432:
                if inputs[10] >= 0.5:
                    var2 = params[40]
                else:
                    var2 = params[41]
            else:
                if inputs[0] >= -0.7030959:
                    var2 = params[42]
                else:
                    var2 = params[43]
        else:
            if inputs[9] >= 0.5:
                if inputs[5] >= 1.39:
                    var2 = params[44]
                else:
                    var2 = params[45]
            else:
                if inputs[2] >= 1.6069634:
                    var2 = params[46]
                else:
                    var2 = params[47]
    if inputs[15] >= -0.5:
        if inputs[0] >= -0.04119027:
            if inputs[9] >= 0.5:
                if inputs[0] >= 0.50546956:
                    var3 = params[48]
                else:
                    var3 = params[49]
            else:
                if inputs[3] >= -0.5621391:
                    var3 = params[50]
                else:
                    var3 = params[51]
        else:
            if inputs[0] >= -0.70321965:
                if inputs[0] >= -0.5651474:
                    var3 = params[52]
                else:
                    var3 = params[53]
            else:
                if inputs[8] >= 0.5:
                    var3 = params[54]
                else:
                    var3 = params[55]
    else:
        if inputs[2] >= 1.0495913:
            if inputs[9] >= 0.5:
                if inputs[0] >= -0.38637096:
                    var3 = params[56]
                else:
                    var3 = params[57]
            else:
                if inputs[3] >= 0.7944947:
                    var3 = params[58]
                else:
                    var3 = params[59]
        else:
            if inputs[9] >= 0.5:
                if inputs[15] >= -1.5:
                    var3 = params[60]
                else:
                    var3 = params[61]
            else:
                if inputs[15] >= -1.5:
                    var3 = params[62]
                else:
                    var3 = params[63]
    if inputs[4] >= -0.1417594:
        if inputs[10] >= 0.5:
            if inputs[4] >= 0.8992201:
                if inputs[2] >= 0.67801005:
                    var4 = params[64]
                else:
                    var4 = params[65]
            else:
                if inputs[0] >= 0.005638009:
                    var4 = params[66]
                else:
                    var4 = params[67]
        else:
            if inputs[0] >= -0.37758678:
                if inputs[15] >= -0.5:
                    var4 = params[68]
                else:
                    var4 = params[69]
            else:
                if inputs[0] >= -0.754007:
                    var4 = params[70]
                else:
                    var4 = params[71]
    else:
        if inputs[8] >= 0.5:
            if inputs[1] >= 0.5857327:
                if inputs[0] >= -0.7034671:
                    var4 = params[72]
                else:
                    var4 = params[73]
            else:
                if inputs[15] >= -0.5:
                    var4 = params[74]
                else:
                    var4 = params[75]
        else:
            if inputs[15] >= 0.5:
                if inputs[7] >= 0.5:
                    var4 = params[76]
                else:
                    var4 = params[77]
            else:
                if inputs[2] >= -0.8083152:
                    var4 = params[78]
                else:
                    var4 = params[79]
    if inputs[15] >= -0.5:
        if inputs[4] >= -1.1827389:
            if inputs[10] >= 0.5:
                if inputs[3] >= -0.5621391:
                    var5 = params[80]
                else:
                    var5 = params[81]
            else:
                if inputs[1] >= -0.17618227:
                    var5 = params[82]
                else:
                    var5 = params[83]
        else:
            if inputs[8] >= 0.5:
                if inputs[10] >= 0.5:
                    var5 = params[84]
                else:
                    var5 = params[85]
            else:
                if inputs[11] >= 0.5:
                    var5 = params[86]
                else:
                    var5 = params[87]
    else:
        if inputs[1] >= 1.3476477:
            if inputs[4] >= -0.1417594:
                var5 = params[88]
            else:
                var5 = params[89]
        else:
            if inputs[7] >= 0.5:
                if inputs[2] >= -0.8083152:
                    var5 = params[90]
                else:
                    var5 = params[91]
            else:
                if inputs[6] >= 0.5:
                    var5 = params[92]
                else:
                    var5 = params[93]
    if inputs[0] >= -0.47594476:
        if inputs[3] >= -0.5621391:
            if inputs[10] >= 0.5:
                if inputs[7] >= 0.5:
                    var6 = params[94]
                else:
                    var6 = params[95]
            else:
                if inputs[4] >= 1.9401996:
                    var6 = params[96]
                else:
                    var6 = params[97]
        else:
            if inputs[8] >= 0.5:
                if inputs[14] >= 2.5:
                    var6 = params[98]
                else:
                    var6 = params[99]
            else:
                if inputs[5] >= -1.385:
                    var6 = params[100]
                else:
                    var6 = params[101]
    else:
        if inputs[0] >= -0.7032815:
            if inputs[1] >= 0.5857327:
                if inputs[0] >= -0.6202649:
                    var6 = params[102]
                else:
                    var6 = params[103]
            else:
                if inputs[0] >= -0.6179142:
                    var6 = params[104]
                else:
                    var6 = params[105]
        else:
            if inputs[15] >= -0.5:
                if inputs[0] >= -0.7549968:
                    var6 = params[106]
                else:
                    var6 = params[107]
            else:
                if inputs[13] >= 0.5:
                    var6 = params[108]
                else:
                    var6 = params[109]
    if inputs[10] >= 0.5:
        if inputs[4] >= -0.66224915:
            if inputs[3] >= -0.5621391:
                if inputs[15] >= -0.5:
                    var7 = params[110]
                else:
                    var7 = params[111]
            else:
                if inputs[2] >= -0.8083152:
                    var7 = params[112]
                else:
                    var7 = params[113]
        else:
            if inputs[0] >= -0.5647762:
                if inputs[0] >= -0.5278456:
                    var7 = params[114]
                else:
                    var7 = params[115]
            else:
                if inputs[0] >= -0.70222986:
                    var7 = params[116]
                else:
                    var7 = params[117]
    else:
        if inputs[4] >= 0.37873033:
            if inputs[0] >= -0.23419455:
                if inputs[15] >= -0.5:
                    var7 = params[118]
                else:
                    var7 = params[119]
            else:
                if inputs[0] >= -0.754007:
                    var7 = params[120]
                else:
                    var7 = params[121]
        else:
            if inputs[0] >= -0.8676444:
                if inputs[2] >= -1.5514779:
                    var7 = params[122]
                else:
                    var7 = params[123]
            else:
                var7 = params[124]
    if inputs[0] >= -0.47464567:
        if inputs[3] >= -0.5621391:
            if inputs[10] >= 0.5:
                if inputs[3] >= 0.7944947:
                    var8 = params[125]
                else:
                    var8 = params[126]
            else:
                if inputs[14] >= 2.5:
                    var8 = params[127]
                else:
                    var8 = params[128]
        else:
            if inputs[8] >= 0.5:
                if inputs[0] >= -0.3537087:
                    var8 = params[129]
                else:
                    var8 = params[130]
            else:
                if inputs[5] >= -1.385:
                    var8 = params[131]
                else:
                    var8 = params[132]
    else:
        if inputs[0] >= -0.7032815:
            if inputs[1] >= 0.5857327:
                if inputs[16] >= 0.5:
                    var8 = params[133]
                else:
                    var8 = params[134]
            else:
                if inputs[0] >= -0.62459517:
                    var8 = params[135]
                else:
                    var8 = params[136]
        else:
            if inputs[5] >= 2.775:
                if inputs[5] >= 5.5550003:
                    var8 = params[137]
                else:
                    var8 = params[138]
            else:
                if inputs[0] >= -0.855891:
                    var8 = params[139]
                else:
                    var8 = params[140]
    if inputs[0] >= -0.47464567:
        if inputs[1] >= 2.4925795:
            if inputs[0] >= 0.38787305:
                var9 = params[141]
            else:
                if inputs[5] >= -4.17:
                    var9 = params[142]
                else:
                    var9 = params[143]
        else:
            if inputs[2] >= 1.0495913:
                if inputs[7] >= 0.5:
                    var9 = params[144]
                else:
                    var9 = params[145]
            else:
                if inputs[10] >= 0.5:
                    var9 = params[146]
                else:
                    var9 = params[147]
    else:
        if inputs[0] >= -0.70321965:
            if inputs[0] >= -0.624224:
                if inputs[1] >= 0.5857327:
                    var9 = params[148]
                else:
                    var9 = params[149]
            else:
                if inputs[10] >= 0.5:
                    var9 = params[150]
                else:
                    var9 = params[151]
        else:
            if inputs[7] >= 0.5:
                if inputs[2] >= -1.1798966:
                    var9 = params[152]
                else:
                    var9 = params[153]
            else:
                if inputs[10] >= 0.5:
                    var9 = params[154]
                else:
                    var9 = params[155]
    return 0.5 + (var0 + var1 + var2 + var3 + var4 + var5 + var6 + var7 + var8 + var9)

def batch_loss(params, inputs, targets):
    error = 0
    for x, y in zip(inputs, targets):
        preds = score(params, x)
        error += (preds - y) ** 2
    return error
