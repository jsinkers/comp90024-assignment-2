<script>
    export let message;
</script>

<div id="info" class="space-y-4">
    <h1>About this visualisation</h1>

    <p>This map shows the SEIFA - IRSAD score for SA2 areas of Greater Melbourne. Election themed tweets are displayed
        as markers coloured by election issue. Tweets opacity represents the intensity of sentiment analysed in the tweet,
        with higher opacity indicating greater intensity.</p>

    <h2>What is SEIFA - IRSAD?</h2>

    <p><b>Socio-Economic Index for Areas (SEIFA)</b> is a measurement by the Australian Bureau of Statistics
        ranking areas on relative socioeconomic advantages and disadvantage. The <b>Index of Relative Socioeconomic
            Advantage and Disadvantage (IRSAD)</b>
        is one of these measurements, and a high IRSAD score indicates a high level of advantage and a low level of disadvantage
        relative to a lower IRSAD score. IRSAD scores shown are based on the 2016 SEIFA.</p>
    <h2>What is SA2?</h2>
    <p> Statistical areas are a structure maintained by the Australian Bureau of Statistics to divide up Australia into useful
        statistical units. SA2s are the second-smallest such area, and are medium-sized areas that correspond to a community
        that interacts socially and economically. SA2s shown are based on 2016 boundaries.</p>

</div>

<style>
    #info {
        @apply font-sans;
    }
    h1 {
        font-size: 2rem;
        text-align: center;
    }

    h2 {
        font-size: 1.25rem;
    }
</style>
