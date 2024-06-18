describe('CARLA Web UI Tests', () => {
    beforeEach(() => {
        // Intercept API calls and mock responses if necessary
        cy.intercept('GET', '/api/carla/world_info', {
            fixture: 'world_info.json',
        });
        cy.intercept('GET', '/api/carla/map_info', {
            fixture: 'map_info.json',
        });
        cy.intercept('DELETE', '/api/carla/destroy/all', {
            body: { "success": "all vehicles destroyed" },
        });
        cy.visit('/');
    });

    it('should display world info correctly', () => {
        cy.contains('Map: Town10');
        cy.contains('Precipitation: 0');
        cy.contains('Wind Intensity: 10');
        cy.contains('Number of Vehicles: 0');
    });


    it('should remove all actors when button is clicked', () => {
        cy.get('button').contains('Remove All Vehicles').click();
        cy.get('.MuiAlert-message').should('not.exist');
    });
});
