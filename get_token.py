#!/usr/bin/env python3
"""
Command line tool to get an access token from the fake CareCloud API.
"""

import click
import requests
import json
import sys
import os

def get_access_token(base_url, grant_type, refresh_token):
    """Get an access token from the fake CareCloud API."""
    
    url = f"{base_url}/oauth2/access_token"
    
    data = {
        "grant_type": grant_type,
        "refresh_token": refresh_token
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        
        token_data = response.json()
        return token_data["access_token"]
        
    except requests.exceptions.ConnectionError:
        click.echo(f"Error: Could not connect to {base_url}", err=True)
        click.echo("Make sure the fake CareCloud API server is running.", err=True)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        click.echo(f"Error: HTTP {response.status_code}", err=True)
        click.echo(f"Response: {response.text}", err=True)
        sys.exit(1)
    except KeyError:
        click.echo("Error: Invalid response format", err=True)
        click.echo(f"Response: {response.text}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@click.command()
@click.option(
    "--url", 
    default=lambda: os.getenv("FAKE_CARECLOUD_URL", "http://localhost:7000"),
    help="Base URL of the fake CareCloud API"
)
@click.option(
    "--grant-type",
    default="refresh_token",
    help="OAuth grant type"
)
@click.option(
    "--refresh-token",
    default="dummy",
    help="Refresh token"
)
@click.option(
    "--export",
    is_flag=True,
    help="Output as export statement for shell"
)
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output as JSON"
)
@click.option(
    "--quiet", "-q",
    is_flag=True,
    help="Only output the token"
)
def main(url, grant_type, refresh_token, export, output_json, quiet):
    """Get an access token from the fake CareCloud API.
    
    Examples:
    
      get_token.py                           # Get token from localhost:7000
      
      get_token.py --url http://localhost:8000  # Get token from custom URL
      
      get_token.py --export                  # Export as environment variable
      
      get_token.py --json                    # Output as JSON
    """
    
    # Get the token
    token = get_access_token(url, grant_type, refresh_token)
    
    # Output in requested format
    if output_json:
        output = json.dumps({
            "access_token": token,
            "token_type": "Bearer"
        }, indent=2)
    elif export:
        output = f"export CARECLOUD_ACCESS_TOKEN={token}"
    elif quiet:
        output = token
    else:
        output = f"Bearer {token}"
    
    click.echo(output)

if __name__ == "__main__":
    main()