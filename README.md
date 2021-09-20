```diff
- THIS PROJECT IS STILL UNDER HEAVY DEVELOPMENT AND IS NOT READY FOR USE -
```
<!-- <h1 align="center" style="color:red;"><b>&otimes;&ensp;THIS PROJECT IS STILL UNDER HEAVY DEVELOPMENT<br>AND IS NOT READY FOR USE&ensp;&otimes;</b></h1> -->

# PyDDNS - Python DDNS for Dreamhost and Cloudflare
PyDDNS is a python based Dynamic Domain Naming Service updater for Dreamhost and Cloudflare.

* [Getting Started](#getting-started)
    * [Requirements](#requirements)
    * [Installation](#installation)
* [Usage](#usage)
    * [Configuration](#configuration)
        * [Dreamhost](#config-dreamhost)
        * [Cloudflare](#config-cloudflare)
    * [How to Run](#howtorun)
    * [Schedule](#schedule)
* [Acknowledgments](#acknowledgments)
* [License](#license)
* [Privacy](#privacy)
* [Donation](#donation)

<a id="getting-started"></a>
## Getting Started

<a id="requirements"></a>
### Requirements

Python 3 with urllib. Should be installed by default, if not use your package manager.

<a id="installation"></a>
### Installation

#### Automated Installation
Run the following command in your terminal:
```bash
curl -s -S -L https://raw.githubusercontent.com/TORQDL/pyddns/master/scripts/install.sh | sh -s -- -v
```

The script also accepts some options:
* `-c <channel>` to use specified channel.
* `-r` to reinstall AdGuard Home;
* `-u` to uninstall AdGuard Home;
* `-v` for verbose output;

Note that options `-r` and `-u` are mutually exclusive.

#### Manual installation
Please read these instructions.

<a id="usage"></a>
## Usage

<a id="configuration"></a>
### Configuration

Configuration is done through JSON in a configuration file. Dreamhost and Cloudflare each use different configuration parameters for authentication, but use the same information for updating your DNS records.

PyDDNS supports updating both IPv4 and IPv6 addresses in DNS using A and AAAA records resspectively. It can update the record using either your public IP address (most common) or the local IP address (less common).

### JSON Configuration Parameters

| Dreamhost Specific    | Description                                 |
| --------------------- | ------------------------------------------- |
| `api_key`             | Your Dreamhost API Key<br><br>Example: `ABCD1234EFGH5678` |

| Cloudflare Specific   | Description                                 |
| --------------------- | ------------------------------------------- |
| `api_token`           | Your Clourflare API Token with Zone.DNS permissions<br><br>Example: `1234567893feefc5f0q5000bfo0c38d90bbeb` |
| `api_key`             | Your Cloudflare Global API Key<br><br>Example: `3feefc5f0q5000bfo0c38d90bbeb123456789` |
| `account_email`       | Your Cloudflare login email address<br><br>Example: `yourname@example.com` |
| `zone_id`             | The Zone ID of the site whose DNS you wish to update<br><br>Example: `5000bfo0c38d90bbeb1234567893feefc5f0q` |
| `proxied`             | Whether or not the domain or subdomain should be proxied through Cloudflare. For more information, see [Cloudflare's Help Center](https://support.cloudflare.com/hc/en-us/articles/200169626)<br><br>Boolean: `true` or `false` |

| Parameters for Both   | Description                                 |
| --------------------- | ------------------------------------------- |
| `domain_or_subdomain` | The domain or subdomain<br><br>Example: `example.com` or `sub.example.com` |
| `ipv4`                | Whether the A record should be updated with an IPv4 address.<br><br>Boolean: `true` or `false` |
| `ipv6`                | Whether the AAAA record should be updated with an IPv6 address.<br><br>Boolean: `true` or `false` |
| `local_ip`            | Whether the local IP address should be used instead of the public IP address. If set to `true`, the local IP address will be used.<br><br>Boolean: `true` or `false` |

<a id="config-dreamhost"></a>
<h3><img src="https://www.dreamhost.com/assets/favicons/favicon-f9ebe354d3e28f93ebaa6523488be0049829393ae313ab3b2e6497952c4f295d.ico" alt="Dreamhost Logo" width="20" height="20">&nbsp;DreamHost</h3>

#### What you will need:

* Dreamhost API Key: you will need your Dreamhost API key, configured for all DNS functions.

> You can get your API key from the [Dreamhost Web Panel](https://panel.dreamhost.com/?tree=home.api). For more information on this, please see the [Dreamhost API Overview](https://help.dreamhost.com/hc/en-us/articles/217560167-API_overview).
> 
> When configuring your API key, please give it access to **All** dns functions:
> 
> - [x] **All** dns functions
> - [ ] dns-add_record
> - [ ] dns-list_records
> - [ ] dns-remove_record
> 
> It should look similar to this in your list of existing API keys after it is created:
> 
> |API KEY         |CREATED            |COMMENT   |FUNCTION ACCESS|ACTIONS              |
> |----------------|-------------------|----------|---------------|---------------------|
> |ABCD1234EFGH5678|2021-09-14 09:41:00|PyDDNS Key|dns-\*         |&otimes;&nbsp;Destroy|

Once you have your API key, you can fill in the `dreamhost.json` configuration file as follows:
```json
{
    "dns": [
        {
            "provider": "dreamhost",
            "authentication": {
                "api_key": "ABCD1234EFGH5678"
            },
            "records": {
                "example.com": {
                    "ipv4": true,
                    "ipv6": true,
                    "local_ip": false
                },
                "sub.example.com": {
                    "ipv4": true,
                    "ipv6": true,
                    "local_ip": false
                }
            }
        }
    ]
}
```

<a id="config-cloudflare"></a>
<h3><img src="https://www.cloudflare.com/favicon.ico" alt="Cloudflare Logo" width="20" height="20">&nbsp;Cloudflare</h3>

[Cloudflare Dashboard](https://dash.cloudflare.com/profile/api-tokens)

```bash
curl -X GET "https://api.cloudflare.com/client/v4/user/tokens/verify" \
     -H "Authorization: Bearer 1234567893feefc5f0q5000bfo0c38d90bbeb" \
     -H "Content-Type:application/json"
```


```json
{
    "dns": [
        {
            "provider": "cloudflare",
            "authentication": {
                "api_token": "1234567893feefc5f0q5000bfo0c38d90bbeb",
                "api_key": "3feefc5f0q5000bfo0c38d90bbeb123456789",
                "account_email": "yourname@example.com"
            },
            "zones": {
                "5000bfo0c38d90bbeb1234567893feefc5f0q": {
                    "records": {
                        "example.com": {
                            "ipv4": true,
                            "ipv6": true,
                            "proxied": true,
                            "local_ip": false
                        },
                        "sub.example.com": {
                            "ipv4": true,
                            "ipv6": true,
                            "proxied": true,
                            "local_ip": false
                        }
                    }
                }
            }
        }
    ]
}
```

<a id="howtorun"></a>
### How to Run

TODO

<a id="schedule"></a>
### Schedule

TODO

<a id="acknowledgments"></a>
## Acknowledgments

PyDDNS was inspired by and uses code from [dreampy_dns](https://github.com/gsiametis/dreampy_dns) by [Georgios Siametis](https://github.com/gsiametis) and [cloudflare-ddns](https://github.com/owenlsa/cloudflare-ddns) by [LLLLnnnn](https://github.com/owenlsa).

<a id="license"></a>
## License

PyDDNS is licensed under the MIT License, a short and simple permissive license with conditions only requiring preservation of copyright and license notices. Licensed works, modifications, and larger works may be distributed under different terms and without source code. This is not legal advice. [Learn more about repository licenses](https://docs.github.com/articles/licensing-a-repository/#disclaimer).

See the PyDDNS [LICENSE](https://github.com/TORQDL/pyddns/blob/master/LICENSE)

<a id="privacy"></a>
## Privacy

PyDDNS does not collect any usage statistics. However, as it connects to and utilizes the Dreamhost and/or Cloudflare APIs, certain information may be collected by Dreamhost and/or Cloudflare per their respective privacy policies and terms of use. Please visit [Dreamhost](https://www.dreamhost.com) and [Cloudflare](https://www.cloudflare.com) for more information.

<a id="donation"></a>
## Donation

TODO

<hr>

```diff
- text in red
+ text in green
! text in orange
# text in gray
@@ text in purple (and bold)@@
```
